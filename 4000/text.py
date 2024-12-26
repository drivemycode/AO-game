import math, random, csv, pygame, os, sys

from typing import Union, Callable, Optional
from pygame import SurfaceType
from pygame.event import event_name
from pygame.locals import *
from cases import CASES_LIST

class Document(pygame.sprite.Sprite):
    """
    Generic class for the "charges" sheet and "evidence" sheet.
    """
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "document.jpeg"))
        self.image = pygame.transform.scale(self.image, (400, 540))
        self.rect = self.image.get_rect()

    def add_content(self, content: dict) -> None:
        """
        Abstract method.
        """
        raise NotImplementedError

    def update(self, event: pygame.event.Event) -> None:
        """
        If clicked on the document comes on top of all the rest.
        """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN and self is not document_group.get_top_sprite():
            pygame.sprite.LayeredUpdates.move_to_front(document_group, self)
            sfx = random.choice(document_sounds)
            sfx.set_volume(0.2)
            sfx.play(fade_ms=100)

    def set_pos(self, x: int, y: int) -> None:
        """
        set the rect.x and rect.y attributes
        """
        self.rect.x, self.rect.y = x, y

    def _get_text_posx(self, surface: SurfaceType) -> int:
        """
        Helper function to return x-coordinate that would center text's x-coordinate
        """
        return self.image.get_width() // 2 - surface.get_width() // 2

    def _get_text_posy(self, surface: SurfaceType) -> int:
        """
        Helper function to return y-coordinate that would center text's x-coordinate
        """
        return self.image.get_height() // 2 - surface.get_height() // 2

    def _blit_long_text(self, text: Union[str, list], coord: tuple[int, int], wbreak=True, bp=False) -> int:
        """
        Blits a paragraph or list of bullet points onto the surface. Note that the thing divided by len(words)
        may be made dependent on the width of the image, but that is untested thus far.

        returns the last height (y) of the last text as reference.

        Note that bp is a flag that is default false (bullet points off by default),
        and wbreak is a flag that determines if word breaking is on (on by default)
        """

        def _wbreak_helper(string: str, end: int, wbreak: bool) -> bool:
            """
            Checks if the last word in the string is part of an ongoing word or
            is the last letter of the word. returns True if a word break is deemed necessary.

            end represents end index in the original text that <string> was part of.
            """
            if not wbreak:
                return False

            if string[-1] == " " or not string[-1].isalpha():
                return False
            else:
                try:
                    text[end]
                except IndexError:
                    return False
                else:
                    return text[end].isalpha()


        (x, y) = coord

        if not bp:
            width = math.ceil(self.image.get_width() * 0.85)
            iterations = 1 + (len(text) * 6 // width)
            for i in range(iterations):
                line = text[i * width // 6 : (i+1) * width // 6]
                temp = "-" if _wbreak_helper(line, (i+1) * width // 6, wbreak) else ""
                words = font4.render(line + temp, 1, "black")
                self.image.blit(words, (x + 20, y))
                y += 16
            return y + 16
        else:
            temp = self._blit_long_text(f"{1}. " + text[0], (x, y), wbreak=wbreak)
            for i in range(len(text) - 1):
                temp = self._blit_long_text(f"{i + 2}. " + text[i + 1], (x, temp), wbreak=wbreak)


class Charges(Document):

    def __init__(self) -> None:
        Document.__init__(self)
        self.rect.x, self.rect.y = 260, 110

    def add_content(self, content: dict) -> None:
        title1 = font2.render("The University of Soronto", 1, "black")
        title2 = font1.render("VS", 1, "black")
        name = font9.render(content["name"], 1, "black")
        self.image.blit(title1, (self._get_text_posx(title1), 33))
        self.image.blit(title2, (self._get_text_posx(title2), 100))
        self.image.blit(name, (self._get_text_posx(name), 166))

        pygame.draw.line(self.image, "black", (0, 233), (self.image.get_width(), 233) )

        charges_title = font3.render("Charges", 1, "black")
        self.image.blit(charges_title, (5, 270))
        charges = content["charges"]
        self._blit_long_text(charges, (20, 300), bp=True)



class Evidence(Document):

    def __init__(self) -> None:
        Document.__init__(self)
        self.image = pygame.image.load(os.path.join("assets", "evidence.png"))
        self.image = pygame.transform.scale(self.image, (500, 600))
        self.rect.x, self.rect.y = 600, 130

    def add_content(self, content: dict) -> None:

        description_title = font2.render("DESCRIPTION", 1, "black")
        self.image.blit(description_title, (self._get_text_posx(description_title), 105))
        y = self._blit_long_text(content["description"], (25, 160))

        testimonies_title = font2.render("EVIDENCE", 1, "black")
        self.image.blit(testimonies_title, (self._get_text_posx(testimonies_title), y - 10))
        self._blit_long_text(content["points"], (30, y + 30), bp=True)

class Profile(Document):

    def __init__(self) -> None:
        Document.__init__(self)
        profiles = os.listdir("assets")
        random_profile = random.choice([profile for profile in profiles if profile.startswith("profile")])
        self.image = pygame.image.load(os.path.join("assets", random_profile))
        self.image = pygame.transform.scale(self.image, (430, 575))
        self.rect.x, self.rect.y = 300, 20

    def add_content(self, content: dict) -> None:
        """
        Note: this is processing information for ONE profile.
        """

        def _get_head_shot(gender: str) -> pygame.surface.Surface:
            """
            Based on the student's gender, return an appropriate headshot
            picture
            """
            heads_path = os.path.join("assets", "heads")
            heads = os.listdir(heads_path)

            if gender == "male" or gender == "female":
                heads = [head for head in heads if head.startswith(gender)]

            return pygame.transform.scale(pygame.image.load(os.path.join(heads_path, random.choice(heads))), (100, 100))

        def _blit_profile_points(unwanted_keys: list, x: int, y: int) -> None:
            """
            x, y represent starting x and y.
            """
            for key in content:
                if key not in unwanted_keys:
                    text = font6.render( key + ": " + content[key], 1, "black")
                    self.image.blit(text, (x, y))
                y += 17

        profile_title = font5.render("Profile: " + content["name"], 1, "black")
        self.image.blit(profile_title, (20, 115))
        headshot = _get_head_shot(content["Gender"])
        self.image.blit(headshot, (20, 150))

        _blit_profile_points(["name", "description", "past_offenses"], 130, 150)

        description_title = font5.render("Character description: ", 1, "black")
        self.image.blit(description_title, (20, 260))
        self._blit_long_text(content["description"], (0, 285))

        past_offenses_title = font5.render("Past offenses: ", 1, "black")
        self.image.blit(past_offenses_title, (20, 400))

        y = 420
        if content["past_offenses"]:
            for offense in content["past_offenses"]:
                text = font7.render(offense["date"] + ": " + offense["offence"] + " in course " + offense["course"], 1, "black")
                self.image.blit(text, (20, y))
                y += 17
        else:
            text = font7.render("No past offenses found.", 1, "black")
            self.image.blit(text, (20, y))

class Media(Document):

    def __init__(self) -> None:
        Document.__init__(self)
        self.rect.x, self.rect.y = 100, 50

    def add_content(self, content: dict) -> None:
        """
        Note: add_content method for Media will actually just change the image itself.
        it takes in the indv element of content["media"], which is just a str

        im so lazy so the content is just gonna be a dict with the id and filename.
        redundant but eh.
        """

        mediapath = os.path.join("assets", "cases", str(content["caseid"]), content["filename"])
        image = pygame.image.load(mediapath)

        width, height = image.get_width(), image.get_height()
        self.image = pygame.Surface([width + 70, height + 70])
        self.image.fill("gray")
        self.image.blit(image, (self._get_text_posx(image), self._get_text_posy(image)))

        factor = 0.125 if width > 2000 and height > 2000 else 0.25 if width > 1000 and height > 1000 else 0.5

        self.image = pygame.transform.scale_by(self.image, factor)

class Button(pygame.sprite.Sprite):
    """
    Generic class for buttons.
    """
    def __init__(self, image_filename: str, callback: Callable, t_width=-1, t_height=-1) -> None:
        """
        Each button has to be image based. you can also pass in t_width and t_height
        if u want it to be transformed.

        """
        super().__init__()
        image = pygame.image.load(image_filename)
        self.callback = callback

        if (t_width, t_height) != (-1, -1):
            image = pygame.transform.scale(image, (t_width, t_height))

        self.image = image
        self.rect = self.image.get_rect()

        image = pygame.transform.rotate(image, random.choice([-10, 10]))
        self.hov = image
        self.org = self.image

        # DecisionButton attribute
        self.type = None

    def update(self, event: pygame.event.Event) -> None:
        """
        NOTE: case_type is the case type that the function case_decision needs in order to
        calculate the score from pressing a decision button.
        """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if isinstance(self, DecisionButton):
                draw_penless_background()
                match self.type:
                    case "pending":
                        screen.blit(pen, (-70, 150))
                    case "innocent":
                        screen.blit(pen, (-70, 250))
                    case "guilty":
                        screen.blit(pen, (-70, 350))

            self.image = self.hov
            if event.type == MOUSEBUTTONDOWN:
                self.callback(self)
                pen_sfx.play(fade_ms=100)
        else:
            self.image = self.org

    def set_pos(self, x: int, y: int) -> None:
        """
        set the rect.x and rect.y attributes
        """
        self.rect.x, self.rect.y = x, y

class DecisionButton(Button):
    """
    The buttons that make up the 3 big buttons: Guilty, innocent or Pending.

    """
    def __init__(self, image_filename: str, callback: Callable, t_width=-1, t_height=-1) -> None:
        Button.__init__(self, image_filename, callback, t_width, t_height)

    def set_type(self, type: str) -> None:
        """
        Set the type of the decision button; only innocent, guilty or pending are possible
        values.
        """

        self.type = type

class Cutscene:
    """
    Generic class for cutscenes.
    """
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.played = False

    def draw(self) -> None:
        screen.blit(table, (0, 0))
        screen.blit(pen, (-100, 50))
        screen.blit(lamp, (1000, -200))

        pygame.draw.rect(screen, "black", (0, 480, 1280, 480))

        dialogue = font9.render(self.text, 1, "white")

        screen.blit(dialogue, (640, 550))

        if not self.played:
            random.choice(grunt_sounds).play(fade_ms=100)
            self.played = True

class CutscenePlayer:
    """
    Plays a sequence of cutscenes.
    """
    def __init__(self, lines: list[str]) -> None:
        """
        Assume that lines is non-empty; lines is an ordered list of lines
        the sequence of cutscenes go in.
        """
        self.cutscenes = []

        for line in lines:
            self.cutscenes.append(Cutscene(line))

        self.curr = self.cutscenes[0]

    def next(self) -> None:
        """
        Based on the current cutscene curr, set curr to the next cutscene (and return
        None). If there is no next cutscene set curr to -1.
        """
        try:
            i = self.cutscenes.index(self.curr)
            self.curr = self.cutscenes[i + 1]
        except ValueError:
            self.curr = -1
        except IndexError:
            self.curr = -1

    def is_over(self) -> bool:
        """
        Returns true if and only if the cutscene player has played all scenes if and only if
        the current scene curr is not -1.
        """
        return self.curr == -1

def setup_decisionbuttons() -> None:
    """
    intialize the decision buttons and add them to the decisionbuttons group :).
    """
    pend_button = DecisionButton(pending_filename, case_decision, 80, 80)
    pend_button.set_type("pending")
    pend_button.set_pos(20, 425)

    inno_button = DecisionButton(inno_filename, case_decision, 80, 80)
    inno_button.set_type("innocent")
    inno_button.set_pos(20, 525)

    guilty_button = DecisionButton(guilty_filename, case_decision, 80, 80)
    guilty_button.set_type("guilty")
    guilty_button.set_pos(20, 625)

    decisionbutton_group.add(pend_button, inno_button, guilty_button)

def setup_game_over_buttons() -> Button:
    """
    Buttons seen when all cases are decided upon. return the reset button
    so we may access it later.
    """
    reset_button = Button(reset_filename, reset_progress, 100, 100)
    reset_button.set_pos(-100, -100)
    gameoverbutton_group.add(reset_button)

    return reset_button

def setup_documents(case: dict) -> None:
    """
    Accept a case from cases_list and process its information to be
    added in the document group.
    """
    charges = Charges()
    charges.add_content(case["body"][0])
    evidence = Evidence()
    evidence.add_content(case["body"][1])

    # assume that one case will have 4 profiles/evidence max.
    prog1 = [(300, 20), (750, 200), (175, 120), (400, 10)]
    prog2 = [(200, 20), (150, 200), (75, 120), (500, 10)]

    if "profiles" in case:
        for content in case["profiles"]:
            random_pos = random.choice(prog1)
            profile = Profile()
            profile.set_pos(*random_pos)
            prog1.remove(random_pos)
            profile.add_content(content)
            document_group.add(profile)

    if case["media"]:
        for content in case["media"]:
            random_pos = random.choice(prog2)
            media = Media()
            media.set_pos(*random_pos)
            prog2.remove(random_pos)
            media.add_content(content)
            document_group.add(media)

    curr_case_filename = os.path.join("data", "curr.txt")
    with open(curr_case_filename, "w") as file:
        file.write(case["id"])

    CASES_LIST.remove(case)
    document_group.add(evidence, charges)

def setup_case() -> Optional[dict]:
    """
    Initiliaze the global variable CASE.
    """
    global CASES_LIST

    if CASES_LIST:
        try:
            with open(os.path.join("data", "curr.txt")) as f:
                s = f.read()
                case = [case for case in CASES_LIST if case["id"] == s][0]
                setup_documents(case)
        except FileNotFoundError or IndexError:
            case = extract_random_case()
    else:
        case = None

    return case

def draw_default_background() -> None:
    """
    Draw the default background with the pen in the left middle of the
    table
    """
    screen.blit(table, (0, 0))
    document_group.draw(screen)
    decisionbutton_group.draw(screen)
    screen.blit(pen, (-100, 50))
    screen.blit(lamp, (1000, -200))

def draw_penless_background() -> None:
    """
    Draw the default background but without the pen
    """

    screen.blit(table, (0, 0))
    document_group.draw(screen)
    decisionbutton_group.draw(screen)
    screen.blit(lamp, (1000, -200))


def draw_game_over_background() -> None:
    """
    This is drawn, alongside the reset progress button once all cases
    are decided upon.
    """
    screen.blit(table, (0, 0))
    screen.blit(pen, (-100, 50))
    screen.blit(lamp, (1000, -60))

    gameoverbutton_group.draw(screen)
    m_text = font2.render("Morality: " + str(MORALITY), 1, "black")
    i_s_text = font2.render("Intern score: " + str(INTERN_SCORE), 1, "black")

    screen.blit(m_text, (300, 400))
    screen.blit(i_s_text, (800, 400))

def update_state() -> tuple[int, int]:
    """
    Remove previously completed cases from history.csv file
    and update INTERN_SCORE and MORALITY by returning what they
    should be.
    """
    global CASES_LIST, CASE_COUNTER

    history_file = os.path.join("data", "history.csv")
    past_case_ids = []

    i_s = 0
    m = 50

    with open(history_file, "r") as file:

        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            past_case_ids.append(int(row["id"]))
            if row["is"][0] == "+":
                i_s += int(row["is"][1:])
            else:
                i_s -= int(row["is"][1:])
            if row["m"][0] == "+":
                m += int(row["m"][1:])
            else:
                m -= int(row["m"][1:])
            CASE_COUNTER += 1

    for nom in past_case_ids:
        case = [case for case in CASES_LIST if int(case["id"]) == nom][0]
        CASES_LIST.remove(case)

    return i_s, m


def extract_random_case() -> Optional[dict]:
    """
    the process of extracting a random case from the cases_list. Also add the
    Charges and Evidence objects into the document group.

    It returns the case itself, and also keeps the case id in a text file called
    curr.txt in the data folder.

    When there are no more cases, None is returned :)
    """
    if CASES_LIST:
        case = random.choice(CASES_LIST)
        setup_documents(case)
        return case
    return

def case_decision(button: DecisionButton) -> None:
    """
    When a decision button is pressed, the player's morality and intern score are calculated
    based on the case type and final decision.
    """
    global CASE, INTERN_SCORE, MORALITY, CASE_COUNTER

    if CASE is None:
        return
    temp = {
        "innocent": "I",
        "guilty": "G",
        "pending": "N",
    }
    decision = temp[button.type]
    case_type = CASE["type"]

    # if case is Innocent or Guilty
    if case_type in "IG":

        # Correct verdict
        if decision == case_type:
            INTERN_SCORE += 1
            i_s = "+1"
            m = "+0"
        else:
            i_s = "+0"
            m = "+0"
    else:
        # Correct pending
        if decision == case_type[-1] and case_type[-1] == "N":
            INTERN_SCORE += 1
            i_s = "+1"
            m = "+1"
        elif decision == case_type[-1]:
            MORALITY += 1
            i_s = "+0"
            m = "+1"
        else:
            MORALITY -= 1
            i_s = "+0"
            m = "-1"

    history_file = os.path.join("data", "history.csv")
    with open(history_file, "a") as file:
        file.write("\n" + CASE["id"] + "," + decision + "," + i_s + "," + m)

    document_group.empty()
    CASE = extract_random_case()
    CASE_COUNTER += 1

def reset_progress(button: Button) -> None:
    """
    This function, linked to the reset button seen in the game over screen,
    yea i carnt write thats about it.
    """
    global CASE, CASES_LIST, CASE_COUNTER

    try:
        curr_filepath = os.path.join("data", "curr.txt")
        os.remove(curr_filepath)
    except FileNotFoundError:
        print("curr.txt not found")
    try:
        with open(os.path.join("data", "history.csv"), "w") as f:
            f.write("id,decision,is,m")
    except FileNotFoundError:
        print("history.csv not found")

    reset_b.set_pos(-100, -100)
    setup_decisionbuttons()

    CASES_LIST = copy_cases_list[:]
    CASE = extract_random_case()
    CASE_COUNTER = 0

def cutscene_check(event: pygame.event.Event) -> None:
    """
    Main loop for checking if certain cutscenes should be playing
    """
    def _checker(player: CutscenePlayer) -> None:
        player.curr.draw()
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.next()

    if CASE_COUNTER == 4 and not test_cutscenes.is_over():
        _checker(test_cutscenes)

    if INTERN_SCORE == 5 and not test2_cutscenes.is_over():
        _checker(test2_cutscenes)


def game_input(events: list[pygame.event.Event]) -> None:
    """
    The main game loop.
    """
    draw_default_background()
    for event in events:
        if event.type is QUIT:
            sys.exit(0)

        # if all cases have been exhausted (will add endings in the future)
        if CASE is None:
            reset_b.set_pos(560, 360)
            decisionbutton_group.empty()
            draw_game_over_background()

        cutscene_check(event)
        document_group.update(event)
        decisionbutton_group.update(event)
        gameoverbutton_group.update(event)

        pygame.display.flip()


pygame.init()
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Council of Academic Integrity")
clock = pygame.time.Clock()

test_cutscenes = CutscenePlayer(["two of us riding nowhere", "spending someones", "hard earned pay"])
test2_cutscenes = CutscenePlayer(["lovely sense of motion", "trying to figure it out", "when i need a reason to wake up", "I FIND YOU TURNING"])

font1 = pygame.font.Font(os.path.join("assets", "Times New Roman.ttf"), 20)
font1.set_bold(True)
font2 = pygame.font.Font(os.path.join("assets", "Times New Roman.ttf"), 35)
font3 = pygame.font.Font(os.path.join("assets", "Times New Roman.ttf"), 17)
font4 = pygame.font.Font(os.path.join("assets", "Times New Roman.ttf"), 12)
font5 = pygame.font.Font(os.path.join("assets", "Capsule Eighty Regular.ttf"), 20)
font5.set_bold(True)
font6 = pygame.font.Font(os.path.join("assets", "Capsule Eighty Regular.ttf"), 13)
font7 = pygame.font.Font(os.path.join("assets", "Capsule Eighty Regular.ttf"), 10)
font8 = pygame.font.Font(os.path.join("assets", "Times New Roman.ttf"), 30)
font9 = pygame.font.Font(os.path.join("assets", "Times New Roman.ttf"), 32)

main1 = os.path.join("assets", "stal.mp3")
select = os.path.join("assets", "select.mp3")
paper2 = os.path.join("assets", "paper2.mp3")
paper3 = os.path.join("assets", "paper3.mp3")
pen_sound = os.path.join("assets", "pen.mp3")
grunt1 = os.path.join("assets", "grunt1.mp3")
grunt2 = os.path.join("assets", "grunt2.mp3")
grunt3 = os.path.join("assets", "grunt3.mp3")
table_filename = os.path.join("assets", "table.jpeg")
lamp_filename = os.path.join("assets", "lamp.png")
pen_filename = os.path.join("assets", "pen.png")
paper_filename = os.path.join("assets", "paper.png")
inno_filename = os.path.join("assets", "innocent.jpg")
guilty_filename = os.path.join("assets", "guilty.jpg")
pending_filename = os.path.join("assets", "pending.jpg")
reset_filename = os.path.join("assets", "reset.png")

pygame.mixer.music.load(main1)
pygame.mixer.music.set_volume(0.10)
pygame.mixer.music.play(-1)

paper1_sfx = pygame.mixer.Sound(select)
pen_sfx = pygame.mixer.Sound(pen_sound)
paper2_sfx = pygame.mixer.Sound(paper2)
paper3_sfx = pygame.mixer.Sound(paper3)
grunt1_sfx = pygame.mixer.Sound(grunt1)
grunt2_sfx = pygame.mixer.Sound(grunt2)
grunt3_sfx = pygame.mixer.Sound(grunt2)

document_sounds = [paper1_sfx, paper2_sfx, paper3_sfx]
grunt_sounds = [grunt1_sfx, grunt2_sfx, grunt3_sfx]

screen = pygame.display.get_surface()
table = pygame.transform.scale(pygame.image.load(table_filename), (1280, 720))
lamp = pygame.transform.scale(pygame.image.load(lamp_filename), (500, 500))
pen = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(pen_filename), (250, 250)), 30)

document_group = pygame.sprite.LayeredUpdates()
decisionbutton_group = pygame.sprite.Group()
gameoverbutton_group = pygame.sprite.Group()

# this is held for ease of resetting game progress
copy_cases_list = CASES_LIST[:]

CASE_COUNTER = 0
INTERN_SCORE, MORALITY = update_state()
CASE = setup_case()
setup_decisionbuttons()
reset_b = setup_game_over_buttons()

while True:
    clock.tick(60)
    game_input(pygame.event.get())
