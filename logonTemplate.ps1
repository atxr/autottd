# Logon script to launch TTD recording

# Parse args from user data
$hash = "REPLACE_HASH"
$bucket = "REPLACE_BUCKET"
$children = $REPLACE_CHILDREN

mkdir $hash
Set-Location $hash
mkdir out

# Fetch the sample and command to run
aws s3 cp "s3://$bucket/todo/$hash.exe" .

# Record trace

if ($children) {
    TTD -out ".\out" -acceptEula -children ".\$hash.exe"
}
else {
    TTD -out ".\out" -acceptEula ".\$hash.exe"
}

# Upload result
Compress-Archive -Path .\out -DestinationPath ".\$hash.zip"
aws s3 cp ".\$hash.zip" "s3://$bucket/done/"
aws s3 rm "s3://$bucket/todo/$hash.exe"

# Clean
Set-Location ..
Remove-Item -Recurse ".\$hash"