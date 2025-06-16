# This script will run successfully after obfuscation
$targetHost = "google.com"
$port = 443
$timeout = 30

# Network test
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $result = $tcpClient.ConnectAsync($targetHost, $port).Wait($timeout * 1000)
    
    if ($result) {
        Write-Host "Connection successful to $targetHost`:$port"
    } else {
        Write-Host "Connection timed out to $targetHost`:$port"
    }
} catch {
    Write-Host "Connection failed: $_"
} finally {
    if ($tcpClient) { $tcpClient.Close() }
}

# File operations
$tempFile = [System.IO.Path]::GetTempFileName()
"Test content" | Out-File -FilePath $tempFile
$content = Get-Content -Path $tempFile
Write-Host "File content: $content"
Remove-Item -Path $tempFile -Force

# Basic system info
$disk = Get-PSDrive C
Write-Host "Free space: $([math]::Round($disk.Free / 1GB, 2)) GB"