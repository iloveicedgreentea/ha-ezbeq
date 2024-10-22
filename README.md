# ha-ezbeq
a home assistant integration to automate EzBEQ functions

## Usage

Blueprint
plex integration
media player
automations

## Services

This exposes a service to load a profile. Point it to the right sensors

You can test with the developer tools by calling the service `ezbeq.load_beq_profile`

```yaml
action: ezbeq.load_beq_profile
data:
  tmdb_sensor: sensor.apple_tv_tmdb_id
  year_sensor: sensor.apple_tv_year
  codec_sensor: sensor.apple_tv_codec
  edition_sensor: sensor.apple_tv_edition_title
  title_sensor: sensor.apple_tv_title
  preferred_author: aron7awol
  slots:
    - 1
  dry_run_mode: false
  skip_search: false

```

`unload_beq_profile` does not need any data


### Load Blueprint

You can add these blueprints to use in automations

Load when the media player starts playing
```yaml
blueprint:
  name: Load EzBEQ Profile
  description: Load a BEQ profile using the EzBEQ integration based on sensor data
  domain: automation
  input:
    trigger_entity:
      name: Trigger Entity
      description: The entity that triggers this automation (e.g., media_player.living_room)
      selector:
        entity:
          domain: media_player
    tmdb_sensor:
      name: TMDB ID Sensor
      description: Sensor that provides the TMDB ID
      selector:
        entity:
          domain: sensor
    year_sensor:
      name: Year Sensor
      description: Sensor that provides the release year
      selector:
        entity:
          domain: sensor
    codec_sensor:
      name: Audio Codec Sensor
      description: Sensor that provides the audio codec
      selector:
        entity:
          domain: sensor
    edition_sensor:
      name: Edition Sensor
      description: Sensor that provides the specific edition (optional)
      default: ""
      selector:
        entity:
          domain: sensor
    title_sensor:
      name: Title Sensor
      description: Sensor that provides the title (optional)
      default: ""
      selector:
        entity:
```

### Unload Blueprint
Trigger unload based on a media player

```yaml
alias: "Unload BEQ Profile when Playback Stops"
description: "Unloads the BEQ profile when media playback stops"
use_blueprint:
  path: ezbeq/unload_beq_profile.yaml
  input:
    trigger_entity: media_player.living_room
    slots: [1, 2]
```