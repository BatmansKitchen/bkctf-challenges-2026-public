# Missing Homework

**Flag:** `bkctf{th3_w31rd3st_b1n4ry_xm1_f0rm4t_l0ll}`

## Solve

1. Decompile the APK using `apktool d hiddenfile.apk`.
2. Extract strings from the AndroidManifest.xml with `strings -e l -n 1 AndroidManifest.xml | grep -E ""`.
3. Decode the extracted base64 string to get the flag.

Im going to make you all actually learn the binary XML format, as was intended by the challenge.
