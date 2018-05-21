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

#include <SoftwareSerial.h>

#define DEVICESTATE_PIN A5
#define SENSORDATA_PIN A4

SoftwareSerial swSer(8, 9); //rx/tx

String inputString = "";         
boolean stringComplete = false;  
boolean DeviceState=false;
double volatile currentRMS;
double volatile voltageRMS;
double volatile power;
double volatile energyc;

unsigned long start_time;
long vr_try=0;
long ack_try=0;
long sample=0;

void setup() {
  // initialize serial:
  swSer.begin(9600);
  Serial.begin(9600);

  pinMode(DEVICESTATE_PIN,INPUT);
  pinMode(SENSORDATA_PIN,INPUT);
  
  Serial.println("Booting Arduino..");
  Serial.flush();
  delay(5000);

  Serial.println("Exiting Arduino Setup..");
}

void loop() {

sample=0;
energyc=0.0;
start_time=millis();
while(digitalRead(DEVICESTATE_PIN))
{
    readCurrentandVoltage(&currentRMS,&voltageRMS);

    power=currentRMS*voltageRMS;
    
    energyc+=power;
    
    Serial.print("Current: ");
    Serial.println(currentRMS);
    Serial.print("Voltage: ");
    Serial.println(voltageRMS);
    
    Serial.print("Power: ");
    Serial.println(power);
    sample++;
    Serial.print("Sample: ");
    Serial.println(sample);
    Serial.print("Sample Time: ");
    Serial.println(millis()-start_time);
    
    if(digitalRead(SENSORDATA_PIN))
    {
        String data="START;"+String(power)+";"+String(energyc/3600,4)+";END";
        swSer.println(data);
        swSer.flush();
        ack_try=0;
        while(digitalRead(SENSORDATA_PIN))
        {
          Serial.println("Waiting for ACK");
          delay(1);
          ack_try++;
          if(ack_try>50)
          {
            break;
          }
        }
    }
    
}


}

double readCurrentandVoltage(double *AmpsRMS, double *VoltsRMS)
{

  int mVperAmp = 185;
  double mVperVolt = 5.469737413; 

  double VPP_current = 0;
  double VPP_voltage = 0;
  double VRMS_current = 0;
  double VRMS_voltage = 0;

  getVPPofCurrentSignal(&VPP_current,&VPP_voltage);
  
  VRMS_current = (VPP_current/2.0) *0.707;
  VRMS_voltage = (VPP_voltage/2.0) *0.707;
  
  *AmpsRMS = (VRMS_current * 1000)/mVperAmp;
  *VoltsRMS = (VRMS_voltage * 1000)/mVperVolt;
 
}

double getVPPofCurrentSignal(double *VPP_current, double *VPP_voltage)
{
  const int CurrentSensorIn = A0;
  const int VoltageSensorIn = A7;
  
  int readValue_current;             
  int readValue_voltage;
  
  int maxValue_current = 0;          // store worst max value here
  int minValue_current = 1024;          // store worst min value here
  
  int maxValue_voltage = 0;          // store worst max value here
  int minValue_voltage = 1024;          // store worst min value here

  
   uint32_t start_time = millis();
   while((millis()-start_time) < 1000) //sample for 1 Sec
   {
       readValue_current = analogRead(CurrentSensorIn);
       readValue_voltage = analogRead(VoltageSensorIn);
       
       if (readValue_current > maxValue_current) 
       {
         
           maxValue_current = readValue_current;
       }
       if (readValue_current < minValue_current) 
       {
          
           minValue_current = readValue_current;
       }

       if (readValue_voltage > maxValue_voltage) 
       {
         
           maxValue_voltage = readValue_voltage;
       }
       if (readValue_voltage < minValue_voltage) 
       {
          
           minValue_voltage = readValue_voltage;
       }
       
   }
   
   
   *VPP_current = ((maxValue_current - minValue_current) * 5.0)/1024.0;
   *VPP_voltage = ((maxValue_voltage - minValue_voltage) * 5.0)/1024.0;
      
}

