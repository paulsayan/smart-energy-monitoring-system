/*

    Smart Energy Monitoring System
    Copyright (C) 2018 - Sayan Paul

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

*/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <FS.h>

#include <SoftwareSerial.h>
#include <Ticker.h>
#include <ArduinoJson.h>

#define DEBUG true

#define POWERDATA 1
#define ENERGYDATA 2

#define RELAY_PIN D1
#define DEVICESTATE_PIN D2
#define SENSORDATA_PIN D3

#define DEVICEDATA_JSON_SIZE (JSON_OBJECT_SIZE(3))
#define DEVICECONFIG_JSON_SIZE (JSON_OBJECT_SIZE(5))

SoftwareSerial swSer(D7, D6, false, 256); //rx/tx
ESP8266WiFiMulti WiFiMulti;
Ticker devicestate_updater;
Ticker devicedata_uploader;

String inputString = "";         
boolean stringComplete = false;
boolean volatile checkDeviceState=false;
boolean volatile uploadDeviceData=false;
boolean volatile start_session=false;
boolean volatile end_session=false;

long readdata_try=0;

struct Device
{
  boolean state;
  double power;
  double energyc;
  int session_id;
};

struct DeviceConfig
{
  String id;
  String authtoken;
  String serverhostname;
  String localapssid;
  String localappwd;
};

Device volatile thisdevice;
DeviceConfig thisdeviceconfig;

//softAP
const char* ssid = "Node Device 1";
const char* password = "abcd1234";

ESP8266WebServer server(80);

void setup() {

    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(RELAY_PIN,OUTPUT);
    pinMode(DEVICESTATE_PIN,OUTPUT);
    pinMode(SENSORDATA_PIN,OUTPUT);

    digitalWrite(RELAY_PIN,LOW);
    digitalWrite(DEVICESTATE_PIN,LOW);
    digitalWrite(SENSORDATA_PIN,LOW);
    
    Serial.begin(9600);
    swSer.begin(9600);
    
    serial_bootmsg();

    init_device();
    setup_wifi_and_server();

    delay(2000);
    devicestate_updater.attach(5,getDeviceStateISR);

    Serial.println("Exiting ESP Setup..");
        
}

void loop() {

if(checkDeviceState)
{
  getDeviceState();
  checkDeviceState=false;  
}

if(thisdevice.state && uploadDeviceData)
{
  readDataFromArduino();
  postRealtimeData();
  uploadDeviceData=false;
}

server.handleClient();

delay(10);

}

void getDeviceStateISR()
{ 
  checkDeviceState=true;
}

void deviceDataUploadISR()
{
  uploadDeviceData=true;
}


void getDeviceState()
{

  if((WiFiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;

        String url="http://"+thisdeviceconfig.serverhostname+"/api/device/"+thisdeviceconfig.id+"/state";
        
        Serial.println(url);
        http.begin(url);

        int httpCode = http.GET();
        ledblink();
        
        if(httpCode > 0) {

            if(httpCode == HTTP_CODE_OK) {

                int len = http.getSize();

                String response=http.getString();
                if(DEBUG) Serial.println("inside getstate()");
                if(DEBUG) Serial.println(response);
                
                bool state=thisdevice.state;
                
                char resp[100];
                response.toCharArray(resp,100);

                if(DEBUG) Serial.print("Resp : ");
                if(DEBUG) Serial.println(resp);
                
                deserializeJSON_forGetState(resp,state);
                
                if(state==true && thisdevice.state==false)
                {
                  thisdevice.state=true;

                  start_session=true;
                  
                  digitalWrite(RELAY_PIN,HIGH);
                  digitalWrite(DEVICESTATE_PIN,HIGH);
                  
                  devicedata_uploader.attach(3,deviceDataUploadISR);
                  
                  if(DEBUG) Serial.println("OFF --> ON");
                }
                else if(state==false  && thisdevice.state==true)
                {
                  thisdevice.state=false;
                  digitalWrite(RELAY_PIN,LOW);
                  digitalWrite(DEVICESTATE_PIN,LOW);

                  devicedata_uploader.detach();

                  end_session=true;
                  
                  if(DEBUG) Serial.println("ON --> OFF");
                }
                else
                {
                  if(DEBUG) Serial.println("No change in state.");
                }
                if(DEBUG) Serial.flush();

            }
        } else {
            if(DEBUG) Serial.printf("Get DeviceState : [HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
    }


    if(start_session)
    {
      while(!startSession())
      {
        yield();
      }
      start_session=false;
    }

    if(end_session)
    {
      while(!endSession())
      {
        yield();
      }
      end_session=false;


      //flush incoming buffer
      Serial.println("Flushing incoming buffer");
      while (swSer.available()) {
        Serial.print(swSer.read());
       }
       Serial.println();
       Serial.println("Flush Done");
      
    
    }

    
}

bool startSession()
{
  
  bool done=false;
  
  if((WiFiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;

        String url="http://"+thisdeviceconfig.serverhostname+"/api/sessions/"+thisdeviceconfig.id;
        http.begin(url);

        char request[10]="{}";
        int httpCode = http.POST(request);
        Serial.println(httpCode);
        
        ledblink();
        
        if(httpCode > 0) {

            if(httpCode == HTTP_CODE_OK) {

                int len = http.getSize();

                String response=http.getString();

                Serial.print("inside startSession() : ");
                Serial.println(response);

                char resp[100];
                response.toCharArray(resp,100);

                deserializeJSON_forStartSession(resp,done);

                Serial.print("Done : ");
                Serial.println(done);

            }
        } else {
            if(DEBUG) Serial.printf("Start Session : [HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
    }

    
  return done;
  
}

bool endSession()
{
  
  bool done=false;
  
  if((WiFiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;
        
        String url="http://"+thisdeviceconfig.serverhostname+"/api/session/"+String(thisdevice.session_id);
        
        Serial.println(url);
        http.begin(url);

        http.addHeader("Accept", "application/json");
        http.addHeader("Content-Type", "application/json");

        char request[100];
        serializeJSON_forEndSession(request,100);
        
        int httpCode = http.POST(request);
        Serial.println(httpCode);
        
        ledblink();
        
        if(httpCode > 0) {

            if(httpCode == HTTP_CODE_OK) {

                int len = http.getSize();

                String response=http.getString();

                Serial.print("inside endSession() : ");
                Serial.println(response);

                char resp[100];
                response.toCharArray(resp,100);

                deserializeJSON_forEndSession(resp,done);

                Serial.print("Done : ");
                Serial.println(done);

            }
        } else {
            if(DEBUG) Serial.printf("End Session : [HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
    }

    
  return done;
  
}

void readDataFromArduino()
{

    digitalWrite(SENSORDATA_PIN,HIGH);
    readdata_try=0;
    
    while(digitalRead(SENSORDATA_PIN))
    {
    while (swSer.available()) {

    // get the new byte:
    char inChar = (char)swSer.read();

    if (inChar == '\n') {
      stringComplete = true;

      if(DEBUG) Serial.print("Command :");
      if(DEBUG) Serial.println(inputString);
      
      String response=parse_command();

      if(DEBUG) Serial.print("Response: ");
      if(DEBUG) Serial.println(response);

      if(!response.equalsIgnoreCase("INVALID_COMMAND"))
      {
        digitalWrite(SENSORDATA_PIN,LOW);
        break;
      }

    }
    else
    {
      inputString += inChar;
    }
    }

    readdata_try++;
    
    if(DEBUG) Serial.print("Trying:readdata -- ");
    if(DEBUG) Serial.println(readdata_try);

    if(readdata_try>100)
    {
      digitalWrite(SENSORDATA_PIN,LOW);
      break;
    }

    yield();
    
    }
  
}

String parse_command()
{
    String response;
    
    if(stringComplete)
    {
    inputString.trim();

    if(inputString.startsWith("START;") && inputString.endsWith(";END"))
    {
      //thisdevice.power=inputString.substring(6).toFloat();
      String *slices=split(inputString,';',4);
      
      thisdevice.power=slices[1].toFloat();
      thisdevice.energyc=slices[2].toFloat();
      
      response="PD_OK";
    }
    else
    {
      response="INVALID_COMMAND";
    }
    
    inputString = "";
    stringComplete = false;
    }

    return response;
  
}

void postRealtimeData()
{

  if((WiFiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;

        String url="http://"+thisdeviceconfig.serverhostname+"/api/device/"+thisdeviceconfig.id+"/realtimedata";
        
        http.begin(url);

        char request[100];
        serializeJSON_forPostRealtimeData(request,100);
        if(DEBUG) Serial.println("From postRealtimeData() :");
        if(DEBUG) Serial.println(request);

        http.addHeader("Accept", "application/json");
        http.addHeader("Content-Type", "application/json");
        
        int httpCode = http.POST(request);
        ledblink();
        
        if(httpCode > 0) {
          
            if(httpCode == HTTP_CODE_OK) {

                int len = http.getSize();

                String response=http.getString();

                if(DEBUG) Serial.print("inside postRealtimeData() : ");
                if(DEBUG) Serial.println(response);

            }
        } else {
            if(DEBUG) Serial.printf("Post RealtimeData : [HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
    }
    
}


bool deserializeJSON_forGetState(char* json, bool &state)
{
    StaticJsonBuffer<DEVICEDATA_JSON_SIZE> jsonBuffer;
    JsonObject& root = jsonBuffer.parseObject(json);

    if(DEBUG) root.printTo(Serial);
    if(DEBUG) Serial.println();
    
    bool result=root["result"];
    
    if(result==true)
    {
      state=root["state"];
    }
    else
    {
      String msg=root["msg"];
      if(DEBUG) Serial.println(msg);
    }
    
    return root.success();
}


void serializeJSON_forPostRealtimeData(char* json, size_t maxSize)
{
    StaticJsonBuffer<DEVICEDATA_JSON_SIZE> jsonBuffer;
    JsonObject& root = jsonBuffer.createObject();
    root["instpower"] = thisdevice.power;
    root["energyc"] = thisdevice.energyc;
    root["sid"] = thisdevice.session_id;
    root.printTo(json, maxSize);
}

bool deserializeJSON_forStartSession(char* json, bool &done)
{
    StaticJsonBuffer<DEVICEDATA_JSON_SIZE> jsonBuffer;
    JsonObject& root = jsonBuffer.parseObject(json);

    root.printTo(Serial);
    Serial.println();
    
    bool result=root["result"];
    
    if(result==true)
    {
      thisdevice.session_id=root["sid"];
      done=true;
    }
    else
    {
      done=false;
    }
    
    return root.success();
}

void serializeJSON_forEndSession(char* json, size_t maxSize)
{
    StaticJsonBuffer<DEVICEDATA_JSON_SIZE> jsonBuffer;
    JsonObject& root = jsonBuffer.createObject();
    root["energyc"] = thisdevice.energyc;
    root.printTo(json, maxSize);
}

bool deserializeJSON_forEndSession(char* json, bool &done)
{
    StaticJsonBuffer<DEVICEDATA_JSON_SIZE> jsonBuffer;
    JsonObject& root = jsonBuffer.parseObject(json);

    root.printTo(Serial);
    Serial.println();
    
    bool result=root["result"];
    
    if(result==true)
    {
      done=true;
    }
    else
    {
      done=false;
    }
    
    return root.success();
}

void serial_bootmsg()
{
  Serial.println("Booting ESP..");
  Serial.flush();
  delay(5000);
}
void init_device()
{
  thisdevice.state=false;
  thisdevice.power=0.0;
  thisdevice.energyc=0.0;//dummy value
  thisdevice.session_id=0;

  SPIFFS.begin();  
  
  if(!load_deviceconfig())
  {
    thisdeviceconfig.id="";
    thisdeviceconfig.authtoken="";
    thisdeviceconfig.serverhostname="";
    thisdeviceconfig.localapssid="";
    thisdeviceconfig.localappwd="";
  }
  
}

void setup_wifi_and_server()
{
  
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP(ssid, password);

  char ssid[100],ssid_pwd[100];
  thisdeviceconfig.localapssid.toCharArray(ssid,100);
  thisdeviceconfig.localappwd.toCharArray(ssid_pwd,100);
  
  WiFiMulti.addAP(ssid, ssid_pwd);
  delay(2000);
  
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.softAPIP());

  server.serveStatic("/", SPIFFS, "/index.html");
  server.serveStatic("/bootstrap.min.css", SPIFFS, "/bootstrap.min.css");
  server.serveStatic("/angularjs.min.js", SPIFFS, "/angularjs.min.js");
  
  server.on("/savedeviceconfig", savedeviceconfigHandler);
  server.on("/loaddeviceconfig", loaddeviceconfigHandler);
  
  server.onNotFound([]() {                              // If the client requests any URI
    if (!handleFileRead(server.uri()))                  // send it if it exists
      server.send(404, "text/plain", "404: Not Found"); // otherwise, respond with a 404 (Not Found) error
  });

  server.begin();
  Serial.println("HTTP server started");
  
}

void loaddeviceconfigHandler()
{
  const size_t buffersize=DEVICECONFIG_JSON_SIZE+170;
  StaticJsonBuffer<buffersize> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  char resp[1000];
  
  if(load_deviceconfig())
  {
    root["result"]=true;
    
    root["deviceid"]=thisdeviceconfig.id;
    root["deviceauthtoken"]=thisdeviceconfig.authtoken;
    root["serverhostname"]=thisdeviceconfig.serverhostname;
    root["localapssid"]=thisdeviceconfig.localapssid;
    root["localappwd"]=thisdeviceconfig.localappwd;
    
    root.printTo(resp,1000);
    
  }
  else
  {
    root["result"]=false;
    root.printTo(resp,1000);

  }
  server.send(200, "application/json", resp);
  
}

void savedeviceconfigHandler()
{
  StaticJsonBuffer<DEVICECONFIG_JSON_SIZE> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  char resp[500];
  
  if(server.arg("deviceid") && server.arg("deviceauthtoken") && server.arg("serverhostname") && server.arg("localapssid") && server.arg("localappwd"))
  {
    thisdeviceconfig.id=server.arg("deviceid");
    thisdeviceconfig.authtoken=server.arg("deviceauthtoken");
    thisdeviceconfig.serverhostname=server.arg("serverhostname");
    thisdeviceconfig.localapssid=server.arg("localapssid");
    thisdeviceconfig.localappwd=server.arg("localappwd");
    Serial.println();
    Serial.println(thisdeviceconfig.id);
    Serial.println(thisdeviceconfig.authtoken);
    Serial.println(thisdeviceconfig.serverhostname);
    Serial.println(thisdeviceconfig.localapssid);
    Serial.println(thisdeviceconfig.localappwd);
    
    save_deviceconfig();

    root["result"]=true;
    root.printTo(resp,500);
    
  }
  else
  {
    root["result"]=false;
    root.printTo(resp,500);
  }

  server.send(200, "application/json", resp);
  
}

void handleNotFound(){

  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);

}

bool handleFileRead(String path) { // send the right file to the client (if it exists)
  Serial.println("handleFileRead: " + path);
  if (path.endsWith("/")) path += "index.html";         // If a folder is requested, send the index file
  String contentType = getContentType(path);            // Get the MIME type
  if (SPIFFS.exists(path)) {                            // If the file exists
    File file = SPIFFS.open(path, "r");                 // Open it
    size_t sent = server.streamFile(file, contentType); // And send it to the client
    file.close();                                       // Then close the file again
    return true;
  }
  Serial.println("\tFile Not Found");
  return false;                                         // If the file doesn't exist, return false
}



String getContentType(String filename){
  if(filename.endsWith(".htm")) return "text/html";
  else if(filename.endsWith(".html")) return "text/html";
  else if(filename.endsWith(".css")) return "text/css";
  else if(filename.endsWith(".js")) return "application/javascript";
  else if(filename.endsWith(".json")) return "application/json";
  else if(filename.endsWith(".png")) return "image/png";
  else if(filename.endsWith(".gif")) return "image/gif";
  else if(filename.endsWith(".jpg")) return "image/jpeg";
  else if(filename.endsWith(".ico")) return "image/x-icon";
  else if(filename.endsWith(".xml")) return "text/xml";
  else if(filename.endsWith(".pdf")) return "application/x-pdf";
  else if(filename.endsWith(".zip")) return "application/x-zip";
  else if(filename.endsWith(".gz")) return "application/x-gzip";
  return "text/plain";
}

bool load_deviceconfig()
{
  String path="config.json";
  const size_t buffersize=DEVICECONFIG_JSON_SIZE+170;
  StaticJsonBuffer<buffersize> jsonBuffer;
  boolean flag=false;
  
    File file = SPIFFS.open(path, "r");

    if (!file)
    {
    Serial.println("No File Exist");
    } 
    else 
    {
      size_t size = file.size();
      if ( size == 0 ) 
      {
        Serial.println("Config file empty !");
      } 
      else 
      {
        std::unique_ptr<char[]> buf (new char[size]);
        file.readBytes(buf.get(), size);
        JsonObject& root = jsonBuffer.parseObject(buf.get());
        if (!root.success()) 
        {
          Serial.println("Impossible to read JSON file");
        } 
        else 
        {
          Serial.println("Config loaded");
          root.printTo(Serial);

          thisdeviceconfig.id=root["id"].as<String>();
          thisdeviceconfig.authtoken=root["authtoken"].as<String>();
          thisdeviceconfig.serverhostname=root["serverhostname"].as<String>();
          thisdeviceconfig.localapssid=root["localapssid"].as<String>();
          thisdeviceconfig.localappwd=root["localappwd"].as<String>();
          flag=true;
        }
      }
      file.close();
   }

   return flag;
   
}

void save_deviceconfig()
{
  String path="config.json";
  const size_t buffersize=DEVICECONFIG_JSON_SIZE+170;
  StaticJsonBuffer<buffersize> jsonBuffer;
  
  JsonObject& root = jsonBuffer.createObject();
  root["id"]=thisdeviceconfig.id;
  root["authtoken"]=thisdeviceconfig.authtoken;
  root["serverhostname"]=thisdeviceconfig.serverhostname;
  root["localapssid"]=thisdeviceconfig.localapssid;
  root["localappwd"]=thisdeviceconfig.localappwd;
  
  File file = SPIFFS.open(path, "w");
  root.printTo(file);
  root.printTo(Serial);
  file.close();
  
}

void ledblink()
{
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
}

String *split(String input,char delim,int numofslices)
{
  String *slices=new String[numofslices];
  int lastindex=0;
  int counter=0;
  
  for(int i=0;i<input.length();i++)
  {
    if(input.substring(i,i+1)==String(delim))
    {
      slices[counter]=input.substring(lastindex,i);
      counter++;
      lastindex=i+1;
    }
    if(i==input.length()-1)
    {
      slices[counter]=input.substring(lastindex,i+1);
    }
  }

  return slices;
  
}

