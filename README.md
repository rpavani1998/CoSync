# CoSync

## Requirements:
- Python version: 3.10.13

## Setup:

1. Create a virtual environment:
   ```
   python3 -m venv env
   ```

2. Activate the virtual environment:
    ```
    source env/bin/activate
    ```

3. Install required packages:
    ```
    pip install -r requirements.txt
    ```

## Execution:
 
To run the RestAPI server , use the following command:
    ```
    python main.py
    ```

# API Endpoints

## \transcribe

#### Request Body
    audio: <file>

#### Response Body
```
{
  "transcription": "I'll be here. You see, theoretically? Yeah. You mean, don't you worry, you carry multiple calendars so you'd ever know? But I do have two, one in the office and one at home. Oh. The weekend after that, I will not be in town. But yeah, as I say to you at a camp here. Yeah. I haven't decided whether I'm doing this yet. It is a bit silly, you know. I wasn't just there. But I've been, um, the"
}↵
```


## /diarization

#### Request Body
audio: <file>

#### Response Body
```
{"speaker_segments": [
    {
      "speaker": "SPEAKER 2",
      "start_time": "0:00:00",
      "transcription": "I'll be here."
    },
    {
      "speaker": "SPEAKER 1",
      "start_time": "0:00:01",
      "transcription": "You see, theoretically?"
    },
    {
      "speaker": "SPEAKER 2",
      "start_time": "0:00:02",
      "transcription": "Yeah."
    },
    {
      "speaker": "SPEAKER 1",
      "start_time": "0:00:03",
      "transcription": "You mean, don't you worry, you carry multiple calendars so you'd ever know?"
    },
    {
      "speaker": "SPEAKER 2",
      "start_time": "0:00:07",
      "transcription": "But I do have two, one in the office and one at home."
    },
    {
      "speaker": "SPEAKER 1",
      "start_time": "0:00:10",
      "transcription": "Oh."
    },
    {
      "speaker": "SPEAKER 2",
      "start_time": "0:00:11",
      "transcription": "The weekend after that, I will not be in town. But yeah, as I say to you at a camp here."
    },
    {
      "speaker": "SPEAKER 1",
      "start_time": "0:00:20",
      "transcription": "Yeah. I haven't decided whether I'm doing this yet. It is a bit silly, you know. I wasn't just there. But I've been, um, the"
    }
  ]
}
```

## \analyze

#### Request Body
text: Yeah. I haven't decided whether I'm doing this yet. It is a bit silly, you know. I wasn't just there. But I've been, um, the

#### Response Body

```
{
  "emotion": {
    "anger": 0.105268,
    "disgust": 0.035664,
    "fear": 0.13443,
    "joy": 0.345568,
    "sadness": 0.315099
  },
  "sentiment": {
    "label": "negative",
    "score": -0.295024
  }
}↵
```