import subprocess

command = "npx ts-node ts_scripts/twitter.ts"
# print(output.decode())  # Salida del script TypeScript

try:
    # Run the command and capture output
    result = subprocess.run(command, capture_output=True, text=True, check=True, shell = True)
    print("✅ TypeScript Output:\n", result. stdout)
    
    if "LoginSuccess" in result.stdout:
        print("✅ Login was successful!")
    else:
        print("❌ Login failed!")

except subprocess.CalledProcessError as e:
    print("❌ Error running TypeScript file:", e.stderr)
    print("❌ Login failed!")
except subprocess.CalledProcessError as e:
    print("❌ Error running TypeScript file:", e.stderr)
    print("❌ Login failed!")