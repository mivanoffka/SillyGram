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

1. /start – intended to show a page that welcomes users when they launch the bot first time and, if neccessary, sign them up.
2. /home – meant to bring user to the very beginning of all the other pages structure if they have lost or an error occured and there is a need to 'relaunch' the bot.

It may be either two separate pages or a single page with combined functionality. 

Actually, there is one more command for one more special page.

3. /controls – opens a special CONTROL page with a list of options for users with master privelegy.

This CONTROL page has a "More" option which leads you to another special page – CUSTOM_CONTROLS. This page is empty by default, but can be redefined by bot developer to contain options that are special for your bot.

Use [SillyPage.Flags](#flags) to mark pages as special and [SillyPage.Pointers](#pointers) if you want to create means of navigations for this pages besides default commands.

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

It is convinient as the actual page marked as special can change, and pointers will always lead you to the relevant one.

#### **Get_format_args function**

...

## **SillyButton**

SillyButton objects represent 

### **SillyActionButton**

...

```py
from sillygram import SillyActionButton, SillyText

button = SillyActionButton(text=SillyText(...))

```
#### **Click handling**

SillyActionButtons are able to produce any kind of action in responce to users' actions. This action is defined by an asyncronous handler function that must accept a SillyManager and a SillyEvent object as its arguments. 

```py
from sillygram import SillyActionButton, SillyText, SillyManager, SillyEvent

async def on_silly_button_click(manager: SillyManager, event: SillyEvent):
    ...

button = SillyActionButton(
    text=SillyText(...),
    on_click=on_silly_button_click
    )
```
It is not neccessary to do the type hinting for the function arguments, but appreciated.

#### **Priveleging**

There are two ways of restricting certain actions in SillyGram:

1. Using the SillyManager.priveleged decorator for the handler

```py
from sillygram import SillyActionButton, SillyText, SillyManager, SillyEvent

@SillyManager.priveleged(value=True)
async def on_silly_button_click(manager: SillyManager, event: SillyEvent):
    ...

```

2. Setting *priveleged* flag for the SillyActionButton. In this case the action will be restricted regardless of the handler being used. However, if the handler has a stricter privelegy, it won't be overcome!

```py
from sillygram import SillyActionButton, SillyText, SillyManager, SillyEvent

async def on_silly_button_click(manager: SillyManager, event: SillyEvent):
    ...

button = SillyActionButton(
    text=SillyText(...),
    on_click=on_silly_button_click
    )
```

*True* value used with both the *SillyManager.priveleged* decorator and SillyActionButton *priveleged* flag stand for the master privelegy. It is however possible to use a non-boolean value for specifying priveleges. Visit [SillyPrivelege](#sillyprivilege) for more information.

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

## **SillyText**

...

## **SillyEvent**

...

## **SillyUser**

...

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








