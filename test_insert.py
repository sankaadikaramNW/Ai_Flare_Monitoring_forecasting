from utils.db import save_flare_data_to_db

# Dummy solar flare event (manually created for testing)
test_data = [{
    "flrID": "TEST-123",                            # Fake ID
    "beginTime": "2025-08-05T12:00:00Z",            # Example timestamps
    "peakTime": "2025-08-05T12:15:00Z",
    "endTime": "2025-08-05T12:30:00Z",
    "classType": "M1.1",                            # Sample class
    "sourceLocation": "N15W33",                     # Sample location
    "activeRegionNum": "AR1234"                     # Sample active region
}]

# Call the DB insert function
save_flare_data_to_db(test_data)
