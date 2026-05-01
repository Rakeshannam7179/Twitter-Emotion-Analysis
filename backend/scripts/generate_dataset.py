import csv
import random

# The j-hartmann model uses 7 emotions: anger, disgust, fear, joy, neutral, sadness, surprise
emotions = {
    'anger': [
        "I am so furious about this new update!",
        "This is the worst customer service I have ever experienced.",
        "Why is everything always broken? I am so mad.",
        "Absolutely ridiculous behavior from this company.",
        "I'm seething with rage right now.",
        "Can't believe they would do something so stupid.",
        "This makes my blood boil.",
        "I hate it when people don't listen.",
        "I could scream, this is so frustrating.",
        "Stop ignoring the community's complaints!",
        "I am extremely disappointed and angry.",
        "This is totally unacceptable!",
        "How dare they charge us for this garbage?",
        "I've about had it with these constant delays.",
        "It's like they're trying to make us mad.",
        "Waste of time and money, I'm livid.",
        "The incompetence is staggering.",
        "I'm done with this service forever.",
        "This is an insult to the users.",
        "Give me a refund right now!"
    ],
    'disgust': [
        "Eww, this is absolutely repulsive.",
        "That smells terrible.",
        "I feel physically sick looking at this.",
        "This is genuinely disgusting behavior.",
        "Yuck, I can't even stand to think about it.",
        "What a gross thing to say online.",
        "Absolutely vile and nasty.",
        "I'm cringing so hard right now.",
        "This food looks moldy and horrifying.",
        "Such toxic and sickening people.",
        "Genuinely nauseating content.",
        "I wish I could unsee that.",
        "That's just foul and inappropriate.",
        "Ugh, that's so oily and gross.",
        "I can't believe people find this appealing.",
        "It's just slimy and weird.",
        "Makes me want to wash my eyes out.",
        "That is just plain wrong on so many levels.",
        "The sheer lack of hygiene is disturbing.",
        "I'm totally grossed out by this."
    ],
    'fear': [
        "I'm terrified of what might happen next.",
        "This news honestly scares me.",
        "What if everything goes wrong tomorrow?",
        "I'm shaking, that was a close call.",
        "Please help, I'm genuinely scared.",
        "The thought of losing this terrifies me.",
        "I have a really bad feeling about this...",
        "I'm terrified to check my bank account.",
        "So worried and anxious right now.",
        "This horror movie is giving me nightmares.",
        "I'm panicking, I don't know what to do.",
        "The uncertainty is paralyzing.",
        "I'm jumpy and on edge all day.",
        "It feels like something is watching me.",
        "I'm dreading the outcome of this meeting.",
        "My heart is racing, I'm so nervous.",
        "I'm afraid to even speak up about it.",
        "The future looks so dark and threatening.",
        "I can't stop worrying about it.",
        "I feel so vulnerable and unsafe."
    ],
    'joy': [
        "I am so incredibly happy today!",
        "This is the best news I've heard all year!!!",
        "Absolutely overjoyed and smiling from ear to ear.",
        "What a wonderful surprise, thank you!",
        "Feeling so blessed and joyful right now.",
        "This made my day so much better.",
        "Yay, we finally did it! So proud of the team.",
        "I couldn't be happier with these results.",
        "This is pure bliss.",
        "Loving every second of this beautiful morning.",
        "Life is amazing right now!",
        "I'm so excited for the weekend!",
        "Everything is finally coming together perfectly.",
        "I feel so lucky to have such great friends.",
        "This is a dream come true.",
        "I'm on cloud nine!",
        "Heart full of happiness and gratitude.",
        "Simply wonderful and delightful.",
        "Couldn't ask for anything more.",
        "Tears of joy streaming down my face!"
    ],
    'neutral': [
        "I bought some milk from the store.",
        "The weather is cloudy today.",
        "Just finishing up some routine work.",
        "I will go to sleep at 10 PM.",
        "This is a blue cup on the table.",
        "Reading a textbook for class.",
        "The train arrived exactly on time.",
        "Here is the link to the document.",
        "I am typing on my keyboard.",
        "The meeting is scheduled for tomorrow.",
        "I walked to the park this morning.",
        "The cat is sleeping on the sofa.",
        "Lunch will be served at noon.",
        "I need to buy some new shoes.",
        "The report is due by Friday.",
        "The water is at room temperature.",
        "I'm listening to a podcast about history.",
        "The bus stops at every corner.",
        "I have two appointments today.",
        "Just checking my emails."
    ],
    'sadness': [
        "I feel so completely heartbroken and lost.",
        "Just crying in my room. This hurts so much.",
        "Why does everything always have to end in tears?",
        "I miss them so much it hurts.",
        "Feeling incredibly depressed and lonely tonight.",
        "This grief is unbearable.",
        "I failed again. I'm so disappointed in myself.",
        "It's hard to find the motivation to get out of bed.",
        "Everything just feels so empty.",
        "A tragic ending to a beautiful story.",
        "I feel so hopeless and forgotten.",
        "Nobody understands how much I'm struggling.",
        "I'm just tired of feeling this way.",
        "The world feels so gray and lifeless.",
        "I keep reliving the same painful memories.",
        "I feel like a burden to everyone around me.",
        "It's hard to even pretend to be okay anymore.",
        "Everything I love seems to slip away.",
        "I'm just a shadow of who I used to be.",
        "The silence is deafening and lonely."
    ],
    'surprise': [
        "Wow! I did not see that coming at all!",
        "Oh my goodness, really?!",
        "I'm in complete shock right now.",
        "What?! That is crazy!",
        "Wait, is this actually happening?",
        "Mind blown. Simply incredible.",
        "I can't believe my eyes!",
        "Whoa, that was completely unexpected.",
        "Didn't expect to run into you here!",
        "Astonishing turn of events!",
        "I'm absolutely speechless.",
        "Where did that come from?!",
        "Total plot twist, I'm stunned.",
        "I was NOT expecting that response.",
        "You've got to be kidding me!",
        "My jaw just dropped.",
        "That's the last thing I thought would happen.",
        "I'm pleasantly surprised by this!",
        "Suddenly, everything changed.",
        "What a bolt from the blue!"
    ]
}

def generate_csv(filename, count=1500):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['text', 'label'])
        
        for _ in range(count):
            label = random.choice(list(emotions.keys()))
            sentence = random.choice(emotions[label])
            
            # Add minor variations
            if random.random() > 0.5:
                sentence += " " + random.choice(["Honestly.", "Wow.", "Just saying.", "Bro.", "Seriously.", "No way.", "Can't believe it.", "For real."])
            if random.random() > 0.8:
                sentence = sentence.upper()
            if random.random() > 0.9:
                # Add some punctuation variations
                sentence += random.choice(["!!!", "...", "?!", "!!"])
                
            writer.writerow([sentence, label])

if __name__ == "__main__":
    generate_csv("data/dataset.csv")
    print("Synthetic dataset generated: data/dataset.csv")
