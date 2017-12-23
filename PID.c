//
// Created by t8399190 on 19/11/2017.
//

#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>
#include <stdio.h>

/**
 * The header file for the countSubStr function.
 */


#define deriv 0.0
#define inter 0.0
#define interMin 0.0
#define interMax 0.0

/**
 * the MyString struct
 */
typedef struct PID
{
    double Kp;
    double Ki;
    double Kd;
    double Derivator;
    double Integrator;
    double IntegratorMin;
    double IntegratorMax;
    double setPoint;
    double error;
    float Ctime;
    float Ptime;
//    double Kp = P;
//    double Ki = I;
//    double Kd = D;
//    double Derivator= Deriv;
//    double Integrator = inter;
//    double IntegratorMin = interMin;
//    double IntegratorMax = interMax;
//    double setPoint = 0.0;
//    double error = 0.0;
} MyPID;

float update(MyPID pid,float currentValue)
{
    pid.Ptime = pid.Ctime;
    pid.Ctime = time(NULL);
    float dT = pid.Ctime-pid.Ptime;
    pid.error=pid.setPoint-currentValue;
    float P = pid.Kp * pid.error;
    float D = pid.Kd * (pid.error-pid.Derivator)/dT;
    pid.Derivator = pid.error;
    pid.Integrator = pid.Integrator + pid.error*dT;
    if (pid.Integrator > pid.IntegratorMax) {
        pid.Integrator = pid.IntegratorMax;
    }
    else if (pid.Integrator < pid.IntegratorMin){
        pid.Integrator = pid.IntegratorMin;
    }
    float I = pid.Integrator * pid.Ki;
    float PIDval = P+I+D;
    return PIDval;
}

void setPoint(MyPID pid, float SetPoint)
{
    pid.setPoint = SetPoint;
    pid.Integrator = 0.0;
    pid.Derivator = 0.0;
    pid.Ptime = time(NULL);
    pid.Ctime = time(NULL);
}

void setIntegrator(MyPID pid, float integrator)
{
    pid.Integrator = integrator;
}

void setDerivator(MyPID pid, float derivator)
{
    pid.Derivator = derivator;
}

void setKp(MyPID pid, float p)
{
    pid.Kp = p;
}

void setKi(MyPID pid, float I)
{
    pid.Ki = I;
}
void setKd(MyPID pid, float D)
{
    pid.Kd = D;
}
float getPoint(MyPID pid)
{
    return pid.setPoint;
}
float getError(MyPID pid)
{
    return pid.error;
}
float getIntegrator(MyPID pid)
{
    return pid.Integrator;
}
float getDerivator(MyPID pid)
{
    return pid.Derivator;
}