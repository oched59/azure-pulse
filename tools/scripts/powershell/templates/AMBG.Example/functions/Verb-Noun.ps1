
function Verb-Noun {
    <#
.SYNOPSIS
This is an overview of the script.

.DESCRIPTION
More detailed description of the script / module.

.PARAMETER FirstParameter
Describe the first parameter.

.PARAMETER SecondParameter
Describe the second parameter.

.EXAMPLE
Verb-Noun -FirstParameter "Hello" -SecondParameter "World"
Describe one example

.EXAMPLE
Verb-Noun -FirstParameter "Hello" -SecondParameter "World"
Describe another example

.NOTES
Author: Your Name
Date:   01/01/2016
Version: 1.0

.LINK
https://github.com/AMBGASG/DATA.AI-Azure-OpenAI-Microsoft-Advisor-Bot/wiki

.COMPONENT
Requires PowerShell Core 7.0 or above
#>
    #Requires -PSEdition Core
    #Requires -Version 7.0

    [CmdletBinding()]
    param (
        [Parameter(
            HelpMessage = 'Help message for the parameter.',
            Mandatory = $true,
            ValueFromPipeline = $true,
            ValueFromPipelineByPropertyName = $true,
            Position = 0
        )]
        [TypeName]
        $FirstParameter,
        [Parameter(
            HelpMessage = 'Help message for the parameter.',
            Mandatory = $true,
            ValueFromPipeline = $true,
            ValueFromPipelineByPropertyName = $true,
            Position = 0
        )]
        [TypeName]
        $SecondParameter
    )

    <# ---------------- Begin main script ---------------- #>

    BEGIN {
        try {
            #region Import Modules
            #endregion Import Modules

            #region Set Variables
            #endregion Set Variables

            #region Set Functions
            #endregion Set Functions
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }

    PROCESS {
        try {
            #region Main Script
            #endregion Main Script
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }

    END {
        try {
            #region Cleanup
            #endregion Cleanup
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }
}