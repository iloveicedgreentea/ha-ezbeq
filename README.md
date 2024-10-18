# ha-ezbeq
a home assistant integration to automate EzBEQ functions


## Services

This exposes a service to load a profile. Point it to the right sensors



### Load Blueprint

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
    dry_run_mode: false
```