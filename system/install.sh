
sudo cp displaybox.service /etc/systemd/system/displaybox.service
sudo cp puzzlebox.service /etc/systemd/system/puzzlebox.service

sudo systemctl daemon-reload
sudo systemctl enable displaybox.service
sudo systemctl start displaybox.service
