# Fairholme Campground Reservation Bot

An automated bot to reserve campsites at Fairholme Campground in Olympic National Park using Recreation.gov.

## Features

- **Automated Reservation**: Automatically checks for campsite availability and books when found
- **Smart Site Selection**: Prioritizes preferred loops and site types based on your preferences
- **Desktop Notifications**: Get notified when reservations are successful
- **Anti-Detection**: Uses rotating user agents and stealth techniques to avoid bot detection
- **Comprehensive Logging**: Detailed logs for monitoring and debugging
- **Colored Output**: Easy-to-read console output with color coding

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Recreation.gov account with valid credentials
- Valid payment method on file

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd camping_reservation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp env_example.txt .env
   ```

4. **Configure your settings**
   Edit the `.env` file with your credentials and preferences:
   ```env
   RECREATION_USERNAME=your_email@example.com
   RECREATION_PASSWORD=your_password
   ```

## Configuration

### Required Settings

- `RECREATION_USERNAME`: Your Recreation.gov email address
- `RECREATION_PASSWORD`: Your Recreation.gov password
- `START_DATE`: Start of desired date range (Month, D(D), YYYY format)
- `END_DATE`: End of desired date range (Month, D(D), YYYY format)

### Optional Settings

You can customize the bot behavior by editing `config.py`:

- **Site Preferences**: Modify `PREFERRED_LOOPS` and `PREFERRED_DATES`
- **Refresh Interval**: Change how often the bot checks for availability
- **Browser Settings**: Enable/disable headless mode
- **Notifications**: Configure desktop notifications

## Usage

### Basic Usage

```bash
python ./src/camping_bot.py
```

### Advanced Usage

1. **Set your dates**: Update the `.env` file with your desired camping dates
2. **Configure preferences**: Edit `config.py` to set your preferred loops
3. **Run the bot**: The bot will continuously check for availability and book when found

### Example Configuration

For a July 2025 camping trip:

```env
START_DATE=July 5, 2025
END_DATE= July 10, 2025
```

## How It Works

1. **Login**: Authenticates with your Recreation.gov credentials
2. **Navigate**: Goes to the Fairholme Campground page
3. **Search**: Enters your desired dates and searches for availability
4. **Analyze**: Finds available sites and selects the best match based on preferences
5. **Book**: Completes the reservation process automatically
6. **Notify**: Sends desktop notification on success

## Logs

The bot creates detailed logs in `camping_bot.log` including:
- Login attempts and results
- Site availability checks
- Reservation attempts
- Error messages and stack traces

## Legal Disclaimer

This bot is provided for educational and personal use only. Users are responsible for:
- Complying with Recreation.gov's terms of service
- Ensuring their use doesn't violate any applicable laws

**Happy Camping! 🏕️** 