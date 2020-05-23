from Star import Star
import os
from PIL import Image, ImageDraw 
from io import BytesIO
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



def starscos():
    #Tomar de star.txt y guardar cada una de las estrellas.
    archivo = open("stars.txt", "r")
    stars = []
    mStars = {}
    for linea in archivo.readlines():
        data = linea.split(' ',6)
        if(len(data)>6):
            data[6] = data[6].replace('\n','').split('; ')
            star = Star(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
            stars.append(star)
            for nombre in data[6]:
                mStars.setdefault(str(nombre),star)
        else:
            stars.append(Star(data[0],data[1],data[2],data[3],data[4],data[5],None))
    archivo.close()

    #Tomar de la carpeta las constelacciones y almacenarlas en un Diccionario.
    basepath = 'constelaciones/'
    constelaciones = {}
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            constelacion = open('constelaciones/'+entry, "r")
            edges = []
            for linea in constelacion.readlines():
                edges.append(linea.replace('\n','').split(','))
            constelacion.close()
            constelaciones.setdefault(str(entry[:entry.find('.txt')]).casefold(),edges)
    return {'stars':stars, 'mStars':mStars, 'constelaciones':constelaciones}

class Sky(object):

    def __init__(self):
        super().__init__()
        sky = starscos()
        self.stars = sky.get('stars')
        self.mStars = sky.get('mStars')
        self.constelaciones = sky.get('constelaciones')
        self.n = 1100
    
    def todasStars(self):
        img = Image.new("RGB", (self.n, self.n)) 
        img1 = ImageDraw.Draw(img)  
        for star in self.stars:
            star_size = round(10.0 / (star.brillo + 2))
            if star_size == 1:
                img.putpixel((star.getX(self.n),star.getY(self.n)), (255,255,255))
            else:
                x0 = star.getX(self.n)-int(star_size/2)
                y0 = star.getY(self.n)-int(star_size/2)
                x1 = star.getX(self.n)+int(star_size/2)
                y1 = star.getY(self.n)+int(star_size/2)
                img1.ellipse((x0,y0,x1,y1), fill='white', outline='white',width=1)
        #img.save('star.png')
        return img

    def todasConstelaciones(self):
        img = self.todasStars()
        img1 = ImageDraw.Draw(img)  
        for key in self.constelaciones:
            for edge in self.constelaciones[key]:
                s1 = self.mStars.get(edge[0])
                s2 = self.mStars.get(edge[1])
                img1.line((s1.getX(self.n), s1.getY(self.n), s2.getX(self.n),
                           s2.getY(self.n)), fill='cyan', width = 2)
        return img

    def unaConstelacion(self,constelacion):
        img = self.todasStars()
        img1 = ImageDraw.Draw(img) 
        cos = self.constelaciones.get(constelacion.casefold())
        if(cos != None):
            for edge in cos:
                s1 = self.mStars.get(edge[0])
                s2 = self.mStars.get(edge[1])
                img1.line((s1.getX(self.n), s1.getY(self.n), s2.getX(self.n),
                           s2.getY(self.n)), fill='cyan', width = 2)
            return img
        else:
            return None


sky = Sky()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def listcons(update, context):
    s = 'Las constelaciones son:'
    for key in sky.constelaciones:
        s += "\n - /"+key
    update.message.reply_text(s)

def constelaciones(update, context):
    img = sky.todasConstelaciones()
    bio = BytesIO()
    bio.name = 'img.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    update.message.reply_photo(photo=bio)

def estrellas(update, context):
    img = sky.todasStars()
    bio = BytesIO()
    bio.name = 'img.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    update.message.reply_photo(photo=bio)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hola, soy Los Astros Bot')
    update.message.reply_text('Escribe /help para ver instrucciones.')
    update.message.reply_text('Desarrollado por Amstrong Monachello, Melyssa Solano, Sebastian Combita.')



def boyero(update, context):
    img = sky.unaConstelacion('boyero')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text('Boyero cuenta con un aspecto humano de grandeza en tamaño, ponienso su vista hacia la Osa Mayor.')

def casiopea(update, context):
    img = sky.unaConstelacion('casiopea')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text('Estas estrellas generan similitud con la silueta de una "W" o "M".')

def cazo(update, context):
    img = sky.unaConstelacion('cazo')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text('Las estrellas que mas se ven desde la Osa mayor, forman un asterismo el cual es llamado CAZO. ')

                             
                             

def cygnet(update, context):
    img = sky.unaConstelacion('cygnet')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text('La cruz del Norte: Así se le llama a estas estrellas por su posición y disposición de estas.')

def geminis(update, context):
    img = sky.unaConstelacion('geminis')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text('Gemini (los mellizos) es la tercera constelación del zodíaco y se encuentra a unos treinta grados al noroeste de Orión.')
        
def hydra(update, context):
    img = sky.unaConstelacion('hydra')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text('Hidra (Constelación). Bella constelación del hemisferio sur, también conocida como la serpiente hembra. Una constelación gigantesca muy importante porque se puede ver casi desde cualquier punto del planeta, a finales de enero tiene lugar su etapa más visible también es conocida como la serpiernte hembra.')



def osamayor(update, context):
    img = sky.unaConstelacion('osamayor')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text('La Osa Mayor (en latín, Ursa Maior; abreviado, UMa), también conocida como el Carro Mayor, es una constelación visible durante todo el año en el hemisferio norte. Entre los aficionados se le conoce con el nombre de "el carro", por la forma que dibujan sus siete estrellas principales, aunque ha recibido otros muchos nombres.')

def osamenor(update, context):
    img = sky.unaConstelacion('osamenor')
    if (img != None):
        bio = BytesIO()
        bio.name = 'img.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        update.message.reply_photo(photo=bio)
        update.message.reply_text(' La Osa Menor (ursa en latín) es una constelación del hemisferio norte. Comparte el mismo nombre que la Osa Mayor, debido a que su cola se asemeja al mango de una cuchara: consta de siete estrellas con la forma de carro; cuatro de ellas forman lo que es la parte honda del carro y las otras tres son el mango del carro')




def help(update, context):
    """Send a message when the command /help is issued."""
    s = ('• /estrellas o escribe "estrellas" para visualizar todas las estrellas.\n'+
    '• /constelaciones o escribe "constelaciones" o "todas" para visualizar las es'+
    'trellas y constelaciones.\n• Si mandas un mensaje con el nombre de la'+
    'constelación podrás ver todas las estrellas y en su defecto la constelación.'+
    '\n• /listcons : lista de costelaciones que te puedo mostrar.')
    update.message.reply_text(s)

def echo(update, context):
    """Echo the user message."""
    print(update.message.text)
    if (update.message.text.upper().find('ESTRELLAS')>=0):
        estrellas(update, context)
    if (update.message.text.upper().find('CONSTELACIONES')>=0 or 
        update.message.text.upper().find('TODAS')>=0):
        constelaciones(update, context)
    for word in update.message.text.split(' '):
        img = sky.unaConstelacion(word)
        if (img != None):
            bio = BytesIO()
            bio.name = 'img.png'
            img.save(bio, 'PNG')
            bio.seek(0)
            update.message.reply_photo(photo=bio)
            if('boyero'==word.casefold()):
                update.message.reply_text('Boyero cuenta con un aspecto humano de grandeza en tamaño, ponienso su vista hacia la Osa Mayor.')
            if('casiopea'==word.casefold()):
                update.message.reply_text('Estas estrellas generan similitud con la silueta de una "W" o "M".')
            if('cazo'==word.casefold()):
                update.message.reply_text('Las estrellas que mas se ven desde la Osa mayor, forman un asterismo el cual es llamado CAZO. ')
            if('cygnet'==word.casefold()):
                update.message.reply_text('La cruz del Norte: Así se le llama a estas estrellas por su posición y disposición de estas.')
            if('geminis'==word.casefold()):
                update.message.reply_text('Gemini (los mellizos) es la tercera constelación del zodíaco y se encuentra a unos treinta grados al noroeste de Orión.')
            if('hydra'==word.casefold()):
                update.message.reply_text('Hidra (Constelación). Bella constelación del hemisferio sur, también conocida como la serpiente hembra. Una constelación gigantesca muy importante porque se puede ver casi desde cualquier punto del planeta, a finales de enero tiene lugar su etapa más visible también es conocida como la serpiernte hembra.')
            if('osamayor'==word.casefold()):
                update.message.reply_text('La Osa Mayor (en latín, Ursa Maior; abreviado, UMa), también conocida como el Carro Mayor, es una constelación visible durante todo el año en el hemisferio norte. Entre los aficionados se le conoce con el nombre de "el carro", por la forma que dibujan sus siete estrellas principales, aunque ha recibido otros muchos nombres.')
            if('osamenor'==word.casefold()):
                update.message.reply_text(' La Osa Menor (ursa en latín) es una constelación del hemisferio norte. Comparte el mismo nombre que la Osa Mayor, debido a que su cola se asemeja al mango de una cuchara: consta de siete estrellas con la forma de carro; cuatro de ellas forman lo que es la parte honda del carro y las otras tres son el mango del carro')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1194962488:AAHf30g6vd4KHzMWlJFKLorfRptqourpM8o", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("listcons", listcons))
    dp.add_handler(CommandHandler("constelaciones", constelaciones))
    dp.add_handler(CommandHandler("estrellas", estrellas))
    dp.add_handler(CommandHandler("boyero", boyero))
    dp.add_handler(CommandHandler("casiopea", casiopea))
    dp.add_handler(CommandHandler("cazo", cazo))
    dp.add_handler(CommandHandler("cygnet", cygnet))
    dp.add_handler(CommandHandler("geminis", geminis))
    dp.add_handler(CommandHandler("hydra", hydra))
    dp.add_handler(CommandHandler("osamayor", osamayor))
    dp.add_handler(CommandHandler("osamenor", osamenor))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

