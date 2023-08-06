# POWERLINE WATSON

A [Powerline](https://powerline.readthedocs.io/en/master/) segment shows the time tracked in [watson](https://github.com/TailorDev/Watson).

By [Miguel de Dios Matias](https://github.com/mdtrooper).

## Installation

### Using pip

```
pip install powerline-watson
```

## Configuration

You can activate the Powerline Slotmachine segment by adding it to your segment configuration,
for example in `.config/powerline/themes/shell/default.json`:

```json
{
    "function": "powerline_watson.status",
    "priority": 30
},
```

It shows a segment with time as hh:mm:ss and tags.

![screenshot powerline_watson](https://raw.githubusercontent.com/mdtrooper/powerline_watson/master/powerline_watson.screenshot.jpg "screenshot powerline_watson")

### Arguments
* **line (string)**: The string to format the content of segment.
  * Default: "{time}({tags})⏲️"
    * **PlaceHolders**:
      * **{time}**: The time elapsed (as hh:mm:ss) in the task.
      * **{start}**: The datetime when started the task.
      * **{tags}**: The list of the tags.
      * **{project}**: The project name.
      * **{human_time}**: The time in human format example 'a minute ago'.
* **notask (string)**: The string to show when watson is stopped.
  * Default: "Free"

## License

Licensed under [the GPL3 License](https://github.com/mdtrooper/powerline_swissarmyknife/blob/master/LICENSE).