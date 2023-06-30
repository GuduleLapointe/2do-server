#!/bin/bash

config_file="ical.cfg"
expire="-2 years"

while IFS= read -r line; do
  line=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')  # Trim leading/trailing whitespace

  if [[ $line =~ "^#" ]]; then
    echo "$line"  # Commented line, output as is
  elif [[ $line =~ "^;" ]]; then
    echo "$line"  # Commented line, output as is
  elif [[ $line =~ ^[[:blank:]]*$ ]]; then
    echo "$line"  # Empty line, output as is
  else
    IFS=',' read -r -a grid_info <<< "$line"  # Split line by comma

    grid_name=${grid_info[0]}
    default_region=${grid_info[1]}
    calendar_url=${grid_info[2]}

    # Follow redirects and retrieve final URL and HTTP response code
    response=$(curl -sL -w "%{http_code},%{url_effective}" -o /dev/null "$calendar_url")
    IFS=',' read -r http_code final_url <<< "$response"

    if [[ $http_code -eq 200 ]]; then
      # HTTP request successful, check if the final URL points to a valid iCalendar file
      temp_file=$(mktemp)
      curl -s "$final_url" -o "$temp_file"

      if grep -q "BEGIN:VCALENDAR" "$temp_file"; then
        # Valid iCalendar file
        last_event_date=$(grep -oP "(?<=DTSTART:)[0-9T]+" "$temp_file" | tail -1)
        one_year_ago=$(date -d "$expire" +%Y%m%dT%H%M%S)

        if [[ $last_event_date < $one_year_ago ]]; then
          echo ";OUTDATED; $grid_name,$default_region,$final_url"
        else
          echo "$grid_name,$default_region,$final_url"
        fi
      else
        # Invalid iCalendar file
        echo ";INVALID ICS; $grid_name,$default_region,$final_url"
      fi

      rm "$temp_file"  # Remove the temporary file
    else
      # HTTP error occurred
      echo "; HTTP ERROR $http_code; $grid_name,$default_region,$final_url"
    fi
  fi
done < "$config_file"
