# Weather Project

## Setup Instructions

### Clone and Setup
Clone the repository to your local machine:
```bash
git clone https://github.com/Srijond/weather_backend.git
cd weather_project

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# install dependencies and run project
pip install Django django-background-tasks
python manage.py migrate

# with 2 differnt consoles
python manage.py process_tasks
python manage.py runserver
```
### Project Info
```bash
It will take around 1 min to create cache for the first time
The cache will be updated periodically after 1 hours

```

# API Documentation

### 1. Get 10 coolest Districts

- **URL**: `/api/coolest_places/`
- **Method**: `GET`


#### Response

- **Success**:
    ```json
    [
      {
        "district": "Dhaka",
        "avg_temp": "26.4"
      },
      {
        "district": "Rajshahi",
        "avg_temp": "22.3"
      },
      {
          "district": "Khulna",
          "avg_temp": "22.4"
        },
        {
          "district": "Comilla",
          "avg_temp": "21.3"
        }
    ]
    ```


---

### 2. Get Friends Location and Destination temperature info

- **URL**: `/api/temperature_info/`
- **Method**: `GET`
- **Example format**: `/api/temperature_info/?location=Dhaka&destination=Rajshahi&Date=2022-11-29`

#### Request

- **Params** (JSON):
    ```json
    {
        "location": "Dhaka",
        "destination": "Rajshahi",
        "Date": "2022-11-29"
    }
    ```

#### Response

- **Success**:
    ```json
    { "Dhaka's temperature": 26.4, "Rajshahi's temperature": 22.3}
    ```