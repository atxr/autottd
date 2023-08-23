param (
    [string]$sample = $( Read-Host "Input the name of the sample to record" ),
    [string]$bucket = $( Read-Host "Input s3 bucket name" ),
    [switch]$children = $false,
    [int]$maxtry = 60
)

$hash = (Get-FileHash $sample).Hash

# Upload sample
aws s3 cp $sample "$bucket/todo/$hash.exe"

# Wait for result
Write-Host "Recording TTD trace in sandbox..."
$out = "$hash.zip"
$try = 0
while ((-Not $finished) -And ($try -lt $maxtry)) {
    $try++
    Start-Sleep -Seconds 1
    Write-Host "aws s3 cp $bucket/done/$out .\$out"
    $finished = [bool]((aws s3 cp "$bucket/done/$out" ".\$out") 2> $null)
}

if ($finished) {
    Write-Host "Sample recorded with autottd, results available in $out"
}
else {
    Write-Host "Failed to record sample"
}