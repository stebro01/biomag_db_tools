# pip3 install pyinstaller

pyinstaller --add-data "pm_settings.json" pm_series_get.py
pyinstaller --add-data "pm_settings.json" pm_project_create.py
pyinstaller --add-data "pm_settings.json" --hidden-import notion.block.database --hidden-import notion.block.embed  --hidden-import notion.block.inline --hidden-import notion.block.upload pm_series_add.py