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
num_speakers: 2

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

## \emotion_metrics

#### Request Body
text: Bolsonaro is the president of Brazil. He speaks for all brazilians. Greta is a climate activist. Their opinions do create a balance that the world needs now
#### Response Body

```
[
    {
        "label": "neutral",
        "score": 0.8166000247001648
    },
    {
        "label": "approval",
        "score": 0.1862563043832779
    },
    {
        "label": "realization",
        "score": 0.03558564558625221
    },
    {
        "label": "admiration",
        "score": 0.010316564701497555
    },
    {
        "label": "optimism",
        "score": 0.007428615819662809
    },
    {
        "label": "disapproval",
        "score": 0.00650643277913332
    },
    {
        "label": "annoyance",
        "score": 0.0057200160808861256
    },
    {
        "label": "disappointment",
        "score": 0.004491161555051804
    },
    {
        "label": "desire",
        "score": 0.00175057677552104
    },
    {
        "label": "confusion",
        "score": 0.0016328543424606323
    },
    {
        "label": "caring",
        "score": 0.001428025308996439
    },
    {
        "label": "gratitude",
        "score": 0.00117161322850734
    },
    {
        "label": "sadness",
        "score": 0.0009360897238366306
    },
    {
        "label": "love",
        "score": 0.000929484551306814
    },
    {
        "label": "joy",
        "score": 0.0008868863806128502
    },
    {
        "label": "disgust",
        "score": 0.0008815750479698181
    },
    {
        "label": "relief",
        "score": 0.0008755961898714304
    },
    {
        "label": "excitement",
        "score": 0.0007358704460784793
    },
    {
        "label": "pride",
        "score": 0.00062166916904971
    },
    {
        "label": "anger",
        "score": 0.0006000178400427103
    },
    {
        "label": "curiosity",
        "score": 0.0005971680511720479
    },
    {
        "label": "amusement",
        "score": 0.0004847384407185018
    },
    {
        "label": "surprise",
        "score": 0.0004211840278003365
    },
    {
        "label": "remorse",
        "score": 0.00034570274874567986
    },
    {
        "label": "fear",
        "score": 0.0002992030349560082
    },
    {
        "label": "embarrassment",
        "score": 0.00025112906587310135
    },
    {
        "label": "nervousness",
        "score": 0.00021308859868440777
    },
    {
        "label": "grief",
        "score": 0.00019342680752743036
    }
]
```

## \stance_detection

#### Request Body
text: I think the new policy is a great step forward. It will definitely improve the overall situation. However, some people might disagree with it and argue that it's unnecessary.
#### Response Body

```
{
    "label": "unrelated",
    "score": 0.8007982969284058
}
```

## \extract_keywords

#### Request Body
text: Broadcom agreed to acquire cloud computing company VMware in a $61 billion (€57bn) cash-and stock deal, massively diversifying the chipmaker’s business and almost tripling its software-related revenue to about 45% of its total sales. By the numbers: VMware shareholders will receive either $142.50 in cash or 0.2520 of a Broadcom share for each VMware stock. Broadcom will also assume $8 billion of VMware's net debt.
#### Response Body
```
{
    "keywords": [
        "Broadcom",
        "cloud computing",
        "VMware",
        "chip",
        "VMware",
        "Broadcom",
        "VMware",
        "Broadcom",
        "VMware"
    ]
}```
