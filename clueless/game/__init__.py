# Game states
GAME_STATE_CREATED = 1
GAME_STATE_STARTED = 2
GAME_STATE_FINISHED = 3

# Turn states
SELECTING_ACTION = 1
MOVING_CHARACTER = 2
MAKING_SUGGESTION = 3
WAITING_ON_SUGGESTION = 4
REFUTING_SUGGESTION = 5
MAKING_ACCUSATION = 6



# IDs for queries (still have to manually change in AJAX command)
GET_VALID_MOVES = 'get-valid-moves'
SELECT_ACCUSATION_CARDS = 'select-accusation-cards'
MAKE_ACCUSATION = 'make-accusation'
SELECT_SUGGESTION_CARDS = 'select-suggestion-cards'
MAKE_SUGGESTION = 'make-suggestion'
