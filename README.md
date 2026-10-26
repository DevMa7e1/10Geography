# 10Geography
10Geograpy is a simple web-application that helps you remember the location of geographical landforms by quizzing you.

### You can try it out [>>> here <<<](https://10geography.vercel.app)

## How do I use it?
To start using 10Geography, all you have to do is [go to its main page](https://10geography.vercel.app) and click on the ***Get Started*** button.

### Adding and removing locations
* To add a location to the randomized list, you have to do enter a name into the *Location name* text input and click on (or drag your cursor around) the map located under the text input. On the right, you will be able to see a preview of the image that will be shown in **Quiz Mode**.

* To remove a location, all you have to do is click on the *Delete* button next to its name. The locations and their *Delete* buttons can be found under the **Add a new location** interface.

### Using Quiz Mode
* In **Quiz Mode**, you are going to have to select the name of the location being shown in the image. The black dot represents the exact point of the location. To select the name of the location, click on the radio button that sits left of the name you want to select. (You have to press the radio button itself, not its label)

* To access **Quiz Mode**, click on the *Go to quiz mode >>>* button that can be found at the top of the page.
* Go exit out of **Quiz Mode**, click on the *Go back >>>* button that can be found at the top of the **Quiz Mode** page.

## What is it built with?
10Geography is built on **Python** and it uses the **Flask** web framework. For processing images, it uses **pyvips**.

The user-facing interface of 10Geography uses **HTML** + **CSS** and **JavaScript** + **JQuery** for its functionality (selecting locations, previewing the location etc.).

10Geography is currently being hosted on **Vercel**.

## How do I host 10Geography myself?
All you have to do is clone the repository and deploy it to Vercel. It * should * work without any other additions/modifications.

Commands:
1. `git clone https://github.com/DevMa7e1/10Geography.git`
2. `npm i -g vercel`
3. `vercel` (optionally with `--prod` for a production deployment)