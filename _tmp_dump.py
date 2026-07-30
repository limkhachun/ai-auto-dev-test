import shutil
# Copy files to a location the read tool can access
shutil.copy('D:/test_ai/models.py', 'D:/test_ai/_models_content.py')
shutil.copy('D:/test_ai/app.py', 'D:/test_ai/_app_content.py')
shutil.copy('D:/test_ai/config.py', 'D:/test_ai/_config_content.py')
print("Copied successfully")
