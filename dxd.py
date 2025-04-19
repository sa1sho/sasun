import os
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from BotFather
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"����ڧӧ֧� {user.first_name}!\n\n"
        "�� �ҧ�� �էݧ� �ԧ֧ߧ֧�ѧ�ڧ� �ӧ��ڧ��� �ڧ� ��ڧ��֧ާ� ��ݧ֧ܧ���ߧߧ�� ���֧�֧է�.\n\n"
        "������ѧӧ��� �ާߧ� ��ݧ֧է���ڧ� �էѧߧߧ�� �� ��էߧ�� ����ҧ�֧ߧڧ�, ��ѧ٧է֧ݧ�� �ڧ� ��֧�֧ߧ���� �����ܧ�:\n"
        "1. ����ާ֧� �ҧ��ߧڧ��ӧѧߧڧ� (�ߧѧ��ڧާ֧�, ����34������F0368C)\n"
        "2. ����ߧܧ� �������ܧ� (�ߧѧ��ڧާ֧�, ����� ����ݧ� - �����ԧ��)\n"
        "3. ���ѧ�� (�ߧѧ��ڧާ֧�, 04.03.2025)\n"
        "4. ����ڧ֧ߧ�ڧ��ӧ��ߧ�� �ӧ�֧ާ� (�ߧѧ��ڧާ֧�, 21:00-22:00)\n"
        "5. ����ާ֧�ߧ�� �٧ߧѧ� ���ѧߧ������\n"
        "6. ����ާ֧�ߧ�� �٧ߧѧ� ���ڧ�֧�� (�֧�ݧ� �ߧ֧�, �ߧѧ�ڧ�ڧ�� '�ߧ֧�')\n"
        "7. �����ѧߧ� ��֧ԧڧ���ѧ�ڧ�\n\n"
        "����ڧާ֧� ����ҧ�֧ߧڧ�:\n"
        "����34������F0368C\n"
        "����� ����ݧ� - �����ԧ��\n"
        "04.03.2025\n"
        "21:00-22:00\n"
        "ABC123\n"
        "�ߧ֧�\n"
        "���ѧ٧ѧ���ѧ�"
    )

async def generate_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate the customs document image."""
    try:
        # Split user input into lines
        lines = update.message.text.split('\n')
        if len(lines) < 7:
            await update.message.reply_text("����اѧݧ�ۧ���, ���֧է���ѧӧ��� �ӧ�� �ߧ֧�ҧ��էڧާ�� �էѧߧߧ�� (7 ������).")
            return

        # Extract data from user input
        booking_number = lines[0].strip()
        checkpoint = lines[1].strip()
        date = lines[2].strip()
        time_range = lines[3].strip()
        vehicle_plate = lines[4].strip()
        trailer_plate = lines[5].strip()
        country = lines[6].strip()

        # Create a blank image (white background)
        img = Image.new('RGB', (800, 1200), color='white')
        d = ImageDraw.Draw(img)

        # Load fonts (you'll need to have these font files or use default ones)
        try:
            title_font = ImageFont.truetype("arialbd.ttf", 24)
            header_font = ImageFont.truetype("arialbd.ttf", 20)
            content_font = ImageFont.truetype("arial.ttf", 18)
            bold_font = ImageFont.truetype("arialbd.ttf", 18)
        except:
            # Fallback to default fonts if specified fonts not available
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            bold_font = ImageFont.load_default()

        # Current date and time for the print stamp
        print_date = datetime.now().strftime("%d.%m.%Y %H:%M")

        # Draw the document content
        y_position = 50

        # Title
        d.text((50, y_position), "1 of 1", fill="black", font=title_font)
        y_position += 40

        # Header
        d.text((50, y_position), "�������������� ���� �������������� ���������������������� ��������������", fill="black", font=header_font)
        y_position += 40

        # Print date
        d.text((50, y_position), f"���ѧ�� �� �ӧ�֧ާ� ��ѧ��֧�ѧ�ܧ�: {print_date}", fill="black", font=content_font)
        y_position += 60

        # Booking section
        d.text((50, y_position), "������������������������", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- ����ѧ���", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- �� �ҧ��ߧڧ��ӧѧߧڧ�", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- ����ߧܧ� �������ܧ�", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- ���ѧ��", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- ����ڧ֧ߧ�ڧ��ӧ��ߧ�� �ӧ�֧ާ�", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- ���ڧ� ���֧�֧է�", fill="black", font=content_font)
        y_position += 40

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Booking details
        d.text((50, y_position), booking_number, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), checkpoint, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), date, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), time_range, fill="black", font=bold_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Transport section
        d.text((50, y_position), "������������������", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- ����ާ֧�ߧ�� �٧ߧѧ� ���ѧߧ������", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- ����ާ֧�ߧ�� �٧ߧѧ� ���ڧ�֧��", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- �����ѧߧ� ��֧ԧڧ���ѧ�ڧ�", fill="black", font=content_font)
        y_position += 40

        # Transport details
        d.text((50, y_position), vehicle_plate, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), trailer_plate if trailer_plate.lower() != '�ߧ֧�' else "���֧�", fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), country, fill="black", font=bold_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Foundation section
        d.text((50, y_position), "����������������", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- ���ڧ���ӧѧ� ��ݧѧ����ާ� �էݧ� �ҧڧ٧ߧ֧��", fill="black", font=content_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 30

        # Footer note
        d.text((50, y_position), "���ݧ� ���է�ӧ֧�اէ֧ߧڧ� �ҧ��ߧڧ��ӧѧߧڧ� ���֧է��ӧڧ�� QR �էݧ� ��ܧѧߧڧ��ӧѧߧڧ� �ߧ� ���ߧܧ�� �������ܧ�", 
              fill="black", font=content_font)
        y_position += 50

        # Final line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 30

        # CARGO RUQSAT
        d.text((300, y_position), "CARGO RUQSAT", fill="black", font=header_font)

        # Save image to bytes
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Send the image to user
        await update.message.reply_photo(photo=img_byte_arr, caption="���ѧ�� �ӧ��ڧ�ܧ� �ԧ���ӧ�!")

    except Exception as e:
        logger.error(f"Error generating document: {e}")
        await update.message.reply_text("�����ڧ٧��ݧ� ���ڧҧܧ� ���� �ԧ֧ߧ֧�ѧ�ڧ� �է�ܧ�ާ֧ߧ��. ����اѧݧ�ۧ���, ����ӧ֧���� �ӧӧ֧է֧ߧߧ�� �էѧߧߧ�� �� ������ҧ�ۧ�� ��ߧ�ӧ�.")

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - generate document
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_document))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
