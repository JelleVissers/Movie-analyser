# Image mask color filtering
___

## 1. set colors

De kleurwaardes voor de mask kan zowel gezet worden doormiddel van een muisklik als door het instellen met behulp van enkel sliders.
De keuren worden worden gefilterd op RGB waarde.

Voor het uitfilteren van de kleuren wordt er gebruik gemaakt van een range van kleuren die een boven en ondergrens gezet.
De kleuren die buiten dit gebied vallen worden door de``cv2.inRange()`` functie eruit gefilterd.

het maken van de mask en het filteren van de kleuren gebeurd door onderstaande code:

```Python
# generate color mask
mask = cv2.inRange(frame, low_array, high_array)

mask = cv2.blur(mask, blur_mask)

# make new image
frame_mask = cv2.bitwise_and(frame, frame, mask=mask)
```

De ```cv2.blur()``` wordt gebruikt voor het filteren van de mask die over de image wordt gelegd zodat de ruis uit de image wordt gefilterd.
Hiernaast wordt er een gebied om het pixels die eruit gefilterd moet worden. Er wordt op deze manier een gebied of interest gecreëerd die later verder verwerkt kan worden

#### 1.1 Sliders

Een mogelijkheid om de kleuren range in te stellen is doormiddel van sliders. Deze sliders zijn gemaakt in ```Tkinter``` doormiddels van de onderstaande functies. In deze functie wordt gebruik om de ondergrens te bepalen van de rode slider

```python
self.red_low_slider = Scale(self.root, from_=0, to=255, length=200, orient=HORIZONTAL)
self.red_low_slider.set(self.low_color[0])
self.red_low_slider.place(x=80, y=40)
```

De ```Scale()``` functie wordt gebruikt om een Scaler aan te maken, doormiddel van de ```orient``` kan de oriëntatie van de slider worden gezet.
Doormiddel van de ```slider.set(self.low_color[0])``` functie wordt er een begin waarde aan de slider gegeven bij het opstarten. Vervolgen wordt de slider doormiddel van ```slider.place(x=80, y=40)``` op de juiste plaats in het scherm geplaatst.

Er zijn in totaal 6 sliders voor het bepalen van de range van de mask. Ieder kleur heeft een aparte slider voor de boven en onder grens van de kleur.

Voor het uitlezen van de slider wordt er gebruik gemaakt van de ```slider.get()``` functie. Deze waardes worden opgeslagen in twee tulps en vervolgens in de settings van de mask geladen.


#### 1.2 Mouse event


## 2. data

#### 2.1 Formaat

#### 2.2 verzenden