# Test script for CloakShell obfuscation
# This script contains various PowerShell features to test different obfuscation techniques

# Variables
$targetHost = "google.com"
$port = 443
$timeout = 30
$verbose = $true

# Function definitions
function Test-NetworkConnection {
    param(
        [string]$hostname,
        [int]$port,
        [int]$timeout
    )
    
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $connection = $tcpClient.BeginConnect($hostname, $port, $null, $null)
        $wait = $connection.AsyncWaitHandle.WaitOne($timeout * 1000, $false)
        
        if ($wait) {
            Write-Output "Connection successful to $hostname`:$port"
            return $true
        } else {
            Write-Output "Connection timed out to $hostname`:$port"
            return $false
        }
    }
    catch {
        Write-Error "Connection failed: $_"
        return $false
    }
    finally {
        if ($tcpClient) { $tcpClient.Close() }
    }
}

function Get-SystemInfo {
    param(
        [switch]$Detailed
    )
    
    $info = @{
        "Hostname" = $env:COMPUTERNAME
        "OS" = (Get-WmiObject Win32_OperatingSystem).Caption
        "Architecture" = $env:PROCESSOR_ARCHITECTURE
        "Memory" = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory
    }
    
    if ($Detailed) {
        $info.Add("Processes", (Get-Process).Count)
        $info.Add("Services", (Get-Service).Count)
    }
    
    return $info
}

# Main execution
Write-Host "Starting network diagnostics..." -ForegroundColor Green

# Get system information first
$systemInfo = Get-SystemInfo -Detailed:$verbose

# Display system information
Write-Host "`nSystem Information:" -ForegroundColor Cyan
foreach ($key in $systemInfo.Keys) {
    Write-Host "$key`: $($systemInfo[$key])"
}

# Test connection
$connectionResult = Test-NetworkConnection -hostname $targetHost -port $port -timeout $timeout

if ($connectionResult) {
    # Create a temporary file
    $tempFile = [System.IO.Path]::GetTempFileName()
    "Connection test completed successfully" | Out-File -FilePath $tempFile
    
    # Read and display the file
    $content = Get-Content -Path $tempFile
    Write-Host "`nLog entry: $content" -ForegroundColor Yellow
    
    # Cleanup
    Remove-Item -Path $tempFile -Force
} else {
    Write-Host "Network diagnostics failed" -ForegroundColor Red
}

# Array operations
$ports = @(80, 443, 8080, 8443)
$services = @{
    "HTTP" = 80
    "HTTPS" = 443
    "Custom1" = 8080
    "Custom2" = 8443
}

# Loop through ports
foreach ($port in $ports) {
    Write-Host "Checking port $port..."
    Start-Sleep -Milliseconds 100
}

# Error handling example
try {
    $result = 1 / 0
} catch {
    Write-Host "Error caught: $_" -ForegroundColor Red
} finally {
    Write-Host "Cleanup completed" -ForegroundColor Gray
}

Write-Host "`nScript execution completed" -ForegroundColor Green 