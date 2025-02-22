# **What is SillyGram?**

SillyGram is a lightweight Python framework for building Telegram bots, built on top of aiogram.

Telegram bots often function similarly to simple GUI applications. While creating such bots isn’t inherently difficult, it typically involves writing a significant amount of repetitive code, which can distract you from focusing on the core business logic.

SillyGram aims to streamline the development process by enabling developers to design bots at a higher level of abstraction.

With SillyGram, you can create bots as a collection of pages and buttons, without worrying about the underlying low-level chat functionalities.

# **Installation**

SillyGram can be easily installed with the help of PIP.

```bash
pip install sillygram
```

# **Quick start & documentation**

...

## **SillyBot**

SillyBot is the core class you need to create a bot with SillyGram. A simplest bot can be created only using a singular SillyBot object and a Telegram bot token gained from [@BotFather](https://t.me/BotFather) – a special Telegram-bot for creating your own bots.

```py
from sillygram import SillyBot

bot = SillyBot(token="YOUR_API_TOKEN")
bot.launch()
```

This, however, will trigger a few warnings in console. That's fine as there are no [pages](#sillypage) included.

```bash
2025-01-19 13:38:04,405 - [WARNING] - _setup_specials - There must be a START page.
2025-01-19 13:38:04,406 - [WARNING] - _setup_specials - There must be a HOME page.
```

You can set up pages and settings by passing them as arguments to SillyBot.

```py
from sillygram import SillyBot, SillyPage, SillySettings

bot = SillyBot(
    token="YOUR_API_TOKEN",
    pages=(SillyPage(...), ...),
    settings=SillySettings(...)
)
```
## **SillyPage**

A SillyGram bot consists of pages represented by SillyPage objects. A collection of those must be passed to a SillyBot object.

Each SillyPage require a name, [text-content](#sillytext) and a set of [buttons](#sillybutton). Optionally you may include some [flags](#flags) and a [function](#get_format_args-function) to determine the format args for the page text-content.

```py
from sillygram import SillyPage, SillyButton, SillyText

page = SillyPage(
    name="Page",
    text=SillyText(...),
    buttons=(SillyButton(...), ...),
    flags=...,
    get_format_args=...
)

```
### **Special pages and bot commands**

To make a SillyGram bot work properly, it must include START and HOME pages.

The goal of SillyGram is to avoid using commands to use the bot. However, Telegram functionality makes it impossible to use no commands at all. So there are a few ones:

1. /start – intended to show a page that welcomes users when they launch the bot first time and, if necessary, sign them up.
2. /home – meant to bring user to the very beginning of all the other pages structure if they have lost or an error occurred and there is a need to 'relaunch' the bot.

It may be either two separate pages or a single page with combined functionality. 

Actually, there is one more command for one more special page.

3. /controls – opens a special CONTROL page with a list of options for users with master privilege.

This CONTROL page has a "More" option which leads you to another special page – CUSTOM_CONTROLS. This page is empty by default, but can be redefined by bot developer to contain options that are special for your bot.

Use [SillyPage.Flags](#flags) to mark pages as special and [SillyPage.Pointers](#pointers) if you want to create means of navigation for this pages besides default commands.

#### **Flags**

To mark pages as special, there are flags included in the SillyPage class.

```
SillyPage.Flags.HOME
SillyPage.Flags.START
SillyPage.Flags.CUSTOM_CONTROLS (cannot be mixed with the previous ones)
SillyPage.Flags.NO (set by default and not mixable with any other)
```

The CONTROL page itself is predefined and its status cannot be given to any other page, so there is no flag for it.

#### **Pointers**

To navigate to special pages with buttons or SillyManager methods, there are pointers included in the SillyPage class. 

```
SillyPage.Pointers.HOME
SillyPage.Pointers.START
SillyPage.Pointers.CONTROLS
SillyPage.Pointers.CUSTOM_CONTROLS
```

It is convenient as the actual page marked as special can change, and pointers will always lead you to the relevant one.

#### **Get_format_args function**

...

## **SillyButton**

SillyButton objects represent a single button [attached to a page](#sillypage).

To use it in Telegram, the lib converts a SillyButton to an InlineButton connected to an InlineKeyboard attached to a Telegram message.

```py
from sillygram import SillyButton, SillyText

button = SillyButton(text=SillyText(...))

```
SillyButton is a parental class of the hierarchy, and you will probably never have to use it as it does not produce any actions when clicked. What you need is its derivatives: [SillyActionButton](#sillyactionbutton), [SillyNavigationButton](#sillynavigationbutton) and [SillyLinkButton](#sillylinkbutton)

### **SillyActionButton**

#### **Click handling**

SillyActionButtons are able to produce any kind of action in response to users' actions. This action is defined by an asynchronous handler function that must accept a SillyManager and a SillyEvent object as its arguments. 

```py
from sillygram import SillyActionButton, SillyText, SillyManager, SillyEvent

async def on_silly_button_click(manager: SillyManager, event: SillyEvent):
    ...

button = SillyActionButton(
    text=SillyText(...),
    on_click=on_silly_button_click
    )
```
Type hinting for the handler arguments is not required but appreciated.

#### **Privileging**

There are two ways of restricting certain actions in SillyGram:

1. Using the SillyManager.privileged decorator for the handler

```py
from sillygram import SillyActionButton, SillyText, SillyManager, SillyEvent

@SillyManager.privileged(value=True)
async def on_silly_button_click(manager: SillyManager, event: SillyEvent):
    ...

```

2. Setting *privileged* flag for the SillyActionButton. In this case the action will be restricted regardless of the handler being used. However, if the handler has a stricter privilege, it won't be overcome!

```py
from sillygram import SillyActionButton, SillyText, SillyManager, SillyEvent

async def on_silly_button_click(manager: SillyManager, event: SillyEvent):
    ...

button = SillyActionButton(
    text=SillyText(...),
    on_click=on_silly_button_click
    )
```

*True* value used with both the *SillyManager.privileged* decorator and SillyActionButton *privileged* flag stand for the master privilege. It is however possible to use a non-boolean value for specifying privileges. Visit [SillyPrivilege](#sillyprivilege) for more information.

### **SillyNavigationButton**

SillyNavigationButtons move users to a page it is linked to. To specify the page you use the page name or, if it is one of the special ones, its [pointer](#pointers).

```py
from sillygram import SillyNavigationButton, SillyPage, SillyText

PAGE_NAME = "PAGE_NAME"

page = SillyPage(name=PAGE_NAME, ...)

button = SillyNavigationButton(
    text=SillyText(...),
    page_name=PAGE_NAME,
)

```
If you need to provide specific format args for the page content when it is called with the button, you may specify *f_args* and *f_kwargs*.

```py
from sillygram import SillyNavigationButton, SillyText

...

button = SillyNavigationButton(
        ...,
        f_args = (...),
        f_kwargs = {...},
)

```

This will rewrite the results of the *get_format_args()* function embedded to the page!

### **SillyLinkButton**

A SillyLinkButton is what you need when you want a button that acts like a URI-link. Moreover, the link will be masked by the SillyText you pass as the button's label.

```py
from sillygram import SillyLinkButton, SillyText

button = SillyLinkButton(text=SillyText("Visit my website!"), uri="https://example.org")

```
When the button is clicked, Telegram will always show a confirmation message to ensure that the use wants to visit the page you provided.

## **SillyText**

SillyGram methods often require a SillyText object in places where you would expect a plain string to be needed. 

It is a wrapper for strings that allows them to be localized for different languages based on current locale of the user.

The locale is set automatically by SillyGram lib since Telegram API provides every user's locale. It is usually defined by the system language, not the language set in the Telegram app.

### **Initializing**

There are 2 ways of setting up a SillyText:

1. Plain text. 

2. Dictionary.

Use plain text when there is no need for the line to be localized.

```py
from sillygram import SillyText

text = SillyText("Hello, world!")

```
Otherwise, initialize SillyText with a dictionary.

```py
from sillygram import SillyText

text = SillyText({
    "en": "Hello, world!",
    "ru": "Привет, мир!",
    ("ro", "mo"): "Salut Lume!"
})
```
The first key-value pair will be considered default and used if user's language code is not present in the dictionary.

Moreover, a collection of several language codes may be used as a single key. This may be useful to deal with languages that are very much alike, e.g. romanian and moldavian.

### **Formatting**

Just like plain strings, SillyText implements *format()* method.

To make a SillyText formattable, include several format placeholders:

```py
from sillygram import SillyText

text = SillyText({
    "en": "Hello, {}!",
    "ru": "Привет, {}!",
    ("ro", "mo"): "Salut {}!"
})
```

**Note that each string you pass must contain the same amount of format placeholders! An exception is raised otherwise.**

You would rarely have to call the *format()* method yourself. Usually it will be called automatically inside other methods that utilize SillyText objects, such as SillyManager.show_page(), SillyManager.show_popup() and others.

Such methods accept optional arguments *f_args* and *f_kwargs* that will be passed to the *format()* method of the SillyText inside.

If you provide an amount of format args that is less then the number of SillyText format placeholders, there will be no exception raised and the empty placeholders will be filled with *?* symbols. There, however, will be a WARNING message logged.

The same goes for the case when the amount of args is greater then required. Redundant args will be ignored and a WARNING message will be logged.

## **SillyEvent**

A SillyEvent object must be provided as the second argument for every [action handling function](#click-handling) in SillyGram.

This class is intended to contain all event information. However, in current versions of SillyGram, it only contains a [SillyUser](#sillyuser) object representing the user who performed the action.

## **SillyUser**

SillyGram represents Telegram users in a form of SillyUser class.

SillyGram events, with the exception of [SillyRegularActivities](#sillyregularactivities), are produced by users, so its' handlers are provided with the SillyUser object as a part of SillyEvent argument.

SillyUser's properties related to user's Telegram account:

1. id (a unique key associated with every Telegram user)
1. nickname (optionally)
1. first_name (optionally)
1. last_name (optionally)
1. language_code

SillyUser's properties related to SillyGram functionality:

1. registration_date
1. last_visit_date
1. is_banned
1. ban_expiration_date (optionally, if is_banned is True)
1. nickname_or_id (returns nickname if it exits, otherwise returns id)
1. [registry](#sillyregistry)

If user has ever interacted with a SillyGram bot, his or her data is saved in database. Every time user interacts with the bot, the information is updated.

You can retrieve a SillyUser object for every user who has ever used your bot with the help of SillyManager and user's nickname or id.

## **SillyManager**

...

### **Communication**

...

### **User input**

...

### **Dialogs**

...

### **Data**

...

#### **Statistics**

...

#### **Users**

...

### **SillyRegistry**

SillyRegistry is a key-value storage attached related to every [SillyUser](#sillyuser). [SillyManager](#sillymanager) has its own SillyRegistry too, which may be considered global.

...

## **SillySettings**

...

### **SillyLabels**

...

### **SillyPrivilege**

...

### **SillyRegularActivities**

...

### **Others settings**

...

## **Controls menu**

...








