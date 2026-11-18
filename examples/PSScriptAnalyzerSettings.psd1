# SPDX-License-Identifier: Apache-2.0
# Example for COD-551 to COD-556: PSScriptAnalyzer 1.25.0 settings.
# Run: Invoke-ScriptAnalyzer -Path . -Recurse -Settings ./PSScriptAnalyzerSettings.psd1
@{
    Severity            = @('Error', 'Warning', 'Information')
    IncludeDefaultRules = $true

    Rules = @{
        # Formatting rules are off by default (COD-551).
        PSPlaceOpenBrace = @{
            Enable             = $true
            OnSameLine         = $true
            NewLineAfter       = $true
            IgnoreOneLineBlock = $true
        }
        PSPlaceCloseBrace = @{
            Enable             = $true
            NewLineAfter       = $false
            IgnoreOneLineBlock = $true
            NoEmptyLineBefore  = $false
        }
        PSUseConsistentIndentation = @{
            Enable              = $true
            Kind                = 'space'
            IndentationSize     = 4
            PipelineIndentation = 'IncreaseIndentationForFirstPipeline'
        }
        PSUseConsistentWhitespace = @{
            Enable          = $true
            CheckOpenBrace  = $true
            CheckOpenParen  = $true
            CheckOperator   = $true
            CheckSeparator  = $true
        }
        PSUseCorrectCasing = @{
            Enable = $true
        }

        # Compatibility: the syntax must parse on Windows PowerShell 5.1 and on PowerShell 7 (COD-550, COD-551).
        PSUseCompatibleSyntax = @{
            Enable         = $true
            TargetVersions = @('5.1', '7.0')
        }

        # Scripts for hosts under App Control (COD-553, COD-556).
        PSUseConstrainedLanguageMode = @{
            Enable = $true
        }
    }
}
