#include "arduinoFFT.h"

/*
These values can be changed in order to evaluate the functions
*/
const uint16_t samples = 128;
const double samplingFrequency = 8.0;
const double f1 = 1.0;
const double f2 = 3.0;
const double amplitude = 1.0;

/*
These are the input and output vectors
Input vectors receive computed results from FFT
*/
double vReal[samples];
double vImag[samples];

/* Create FFT object */
ArduinoFFT<double> FFT = ArduinoFFT<double>(vReal, vImag, samples, samplingFrequency);

#define SCL_INDEX     0x00
#define SCL_TIME      0x01
#define SCL_FREQUENCY 0x02


void setup()
{
  Serial.begin(115200); 
  while(!Serial); 
  Serial.println("Ready");
}

void loop()
{

  /* Build raw data */
  for (uint16_t i = 0; i < samples; i++)
  {
    double t = (double)i / samplingFrequency;
    vReal[i] = amplitude * (cos(2 * PI * f1 * t) + cos(2 * PI * f2 * t));
    vImag[i] = 0.0;
  }

  Serial.println("Data:");
  PrintVector(vReal, samples, SCL_TIME);

  FFT.windowing(FFTWindow::Rectangle, FFTDirection::Forward);

  FFT.compute(FFTDirection::Forward);

  Serial.println("Computed Real values:");
  PrintVector(vReal, samples, SCL_INDEX);

  Serial.println("Computed Imaginary values:");
  PrintVector(vImag, samples, SCL_INDEX);

  FFT.complexToMagnitude();

  Serial.println("Computed magnitudes:");
  PrintVector(vReal, samples / 2, SCL_FREQUENCY);

  double x = FFT.majorPeak();
  Serial.println(x, 6);
  
}

void PrintVector(double *vData, uint16_t bufferSize, uint8_t scaleType)
{
  for (uint16_t i = 0; i < bufferSize; i++)
  {
    double abscissa;

    switch (scaleType)
    {
      case SCL_INDEX:
        abscissa = i;
        break;

      case SCL_TIME:
        abscissa = i / samplingFrequency;
        break;

      case SCL_FREQUENCY:
        abscissa = (i * samplingFrequency) / samples;
        break;
    }

    Serial.print(abscissa, 6);
    if (scaleType == SCL_FREQUENCY)
      Serial.print("Hz");
    Serial.print(" ");
    Serial.println(vData[i], 4);
  }
  Serial.println();
  
}

