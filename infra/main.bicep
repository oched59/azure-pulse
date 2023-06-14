// Parameters
@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

// Variables
var abbrs = loadJsonContent('abbreviations.json')

// Resources


// Modules


// Outputs

