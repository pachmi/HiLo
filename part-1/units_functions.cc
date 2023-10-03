// Daniel Thibault
// daniel.thibault@csu.fullerton.edu
// @JustDanielThanks
// Partners: @pachmi

#include "units_functions.h"

// Convert milliliters to teaspoons
double MlToTsp(double volume) {
  // X: Convert milliliters to teaspoons
  // Remember, dividing milliliters by 4.929 will convert milliliters to
  // teaspoons.
  volume = (volume / 4.929);
  return volume;
}

// Convert milliliters to tablespoons
double MlToTbsp(double volume) {
  // X: Convert milliliters to tablespoons
  // Remember, if you convert milliliters to teaspoons first, you can divide
  // teaspoons by 3 to find the number of tablespoons
  volume = MlToTsp(volume);
  volume = (volume / 3);
  return volume;
}

// Convert milliliters to fluid ounces
double MlToOz(double volume) {
  // X: Convert milliliters to fluid ounces
  // Remember, that if you convert to tablespoons first, you can divide
  // tablesppons by 2 to find the number of ounces
  volume = MlToTbsp(volume);
  volume = (volume / 2);
  return volume;
}

// Convert milliliters to cups
double MlToCup(double volume) {
  // X: Convert milliliters to cups
  // Remember, that if you convert to fluid ounces first, you can divide by 8 to
  // find the number of cups
  volume = MlToOz(volume);
  volume = (volume / 8);
  return volume;
}