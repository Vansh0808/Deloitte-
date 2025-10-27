import json
from datetime import datetime

def convert_from_format_1(data):
    """
    Convert data from format 1 to unified format
    - Convert ISO timestamp to milliseconds
    - Rename 'temp' to 'temperature'
    - Rename 'hum' to 'humidity'
    """
    converted_data = []
    
    for item in data:
        # Convert ISO timestamp to milliseconds
        iso_timestamp = item["timestamp"]
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        timestamp_ms = int(dt.timestamp() * 1000)
        
        # Create new item with unified format
        new_item = {
            "timestamp": timestamp_ms,
            "temperature": item["temp"],
            "humidity": item["hum"]
        }
        converted_data.append(new_item)
    
    return converted_data

def convert_from_format_2(data):
    """
    Convert data from format 2 to unified format
    - Data already uses millisecond timestamps
    - Rename 'temperature_c' to 'temperature'
    - Rename 'humidity_percent' to 'humidity'
    """
    converted_data = []
    
    for item in data:
        # Create new item with unified format
        new_item = {
            "timestamp": item["time"],
            "temperature": item["temperature_c"],
            "humidity": item["humidity_percent"]
        }
        converted_data.append(new_item)
    
    return converted_data

def main():
    """Main function to read, convert, merge, and save telemetry data"""
    try:
        # Read input JSON files
        with open('data-1.json', 'r') as file:
            data1 = json.load(file)
        
        with open('data-2.json', 'r') as file:
            data2 = json.load(file)
        
        # Convert both datasets to unified format
        converted_data1 = convert_from_format_1(data1)
        converted_data2 = convert_from_format_2(data2)
        
        # Merge both datasets
        merged_data = converted_data1 + converted_data2
        
        # Sort by timestamp in ascending order
        merged_data.sort(key=lambda x: x["timestamp"])
        
        # Save unified data to output file
        with open('data-result.json', 'w') as file:
            json.dump(merged_data, file, indent=2)
        
        print("✅ Conversion complete! Unified data written to data-result.json")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
