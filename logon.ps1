# Logon script to launch TTD recording

# Parse args from user data
# TODO get sample, bucket, children

# Useful strings 
$sample_name = $sample.Substring($sample.lastIndexOf('.') + 1)
$out = ".\" + $sample_name + ".zip"

# Verify required tools
#TODO

# Fetch the sample and command to run
aws s3 cp $bucket/todo/$sample -OutFile .\sample.exe

# Record trace
mkdir out
TTD.exe -o out .\sample.exe

# Upload result
Compress-Archive -Path .\out -DestinationPath sample.zip
aws s3 cp sample.zip $bucket/done/$out

# Clean
Remove-Item -Recurse .\sample.exe,.\sample.zip,.\out