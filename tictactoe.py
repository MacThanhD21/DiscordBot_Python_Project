import asyncio

BLANK = "BLANK"
pos_1 = 0
pos_2 = 1
pos_3 = 2   
pos_4 = 3
pos_5 = 4
pos_6 = 5
pos_7 = 6
pos_8 = 7
pos_9 = 8
reaction_emojis = ['1️⃣', '2️⃣', '3️⃣',
                   '4️⃣', '5️⃣', '6️⃣',
                   '7️⃣', '8️⃣', '9️⃣', '❌']

async def tictactoe(ctx, bot):
    emojis = ['1️⃣', '2️⃣', '3️⃣', 
              '4️⃣', '5️⃣', '6️⃣', 
              '7️⃣', '8️⃣', '9️⃣', '❌']
    board = [BLANK, BLANK, BLANK, 
             BLANK, BLANK, BLANK, 
             BLANK, BLANK, BLANK]
    current_player = 1
    player_1 = await get_user_char(ctx, bot, current_player)
    player_2 = await get_user_char(ctx, bot, current_player + 1)
    if player_1 == player_2:
        await ctx.send("Player 2 cannot choose the same character as Player 1.")
        return
    await ctx.channel.purge(limit=3)
    def check_not_bot(reaction, user):
        return user != bot.user
    await ctx.send(f'Player1 choose {player_1}. Player2 choose {player_2}') 
    while check_win(player_1, player_2, board) == BLANK and BLANK in board:
        await ctx.send(f"Player {current_player}'s turn.")
        msg = await ctx.send(print_board(player_1, player_2, board))
        for i in range(len(emojis)):
            await msg.add_reaction(emojis[i])   
        reaction, user = await bot.wait_for('reaction_add', timeout=1000.0, check=check_not_bot)
        if reaction.emoji == '❌':
            print("Closing game.")
            return
        else:
            if current_player % 2 == 1:
                make_move(reaction.emoji, emojis, player_1, board)
            else:
                make_move(reaction.emoji, emojis, player_2, board)  
            await ctx.channel.purge(limit=2)
        current_player += 1
        if current_player > 2:
            current_player = 1
    if check_win(player_1, player_2, board) == BLANK:
        msg = await ctx.send(print_board(player_1, player_2, board))
        await ctx.send("It's a tie!")
    else:
        if check_win(player_1, player_2, board) == player_1:
            msg = await ctx.send(print_board(player_1, player_2, board))
            await ctx.send("Player 1 wins!")
        else:
            msg = await ctx.send(print_board(player_1, player_2, board))
            await ctx.send("Player 2 wins!")


def make_move(emoji, emoji_list, player, board):
    for idx in range(len(reaction_emojis)):
        if reaction_emojis[idx] == emoji:
            board[idx] = player
            emoji_list.remove(emoji)
            break


def check_direction(pos1, pos2, pos3, player1, player2, board):
    if (board[pos1] == board[pos2] and board[pos2] == board[pos3]) and (board[pos3] != BLANK):
        if board[pos1] == player1:
            return player1
        elif board[pos1] == player2:
            return player2
    else:
        return BLANK  


def check_win(player1, player2, board):
    lineHOne = check_direction(pos_1, pos_2, pos_3, player1, player2, board)
    if lineHOne != BLANK:
        return lineHOne 
    lineHTwo = check_direction(pos_4, pos_5, pos_6, player1, player2, board)
    if lineHTwo != BLANK:
        return lineHTwo
    lineHThree = check_direction(pos_7, pos_8, pos_9, player1, player2, board)
    if lineHThree != BLANK:
        return lineHThree
    lineVOne = check_direction(pos_1, pos_4, pos_7, player1, player2, board)
    if lineVOne != BLANK:
        return lineVOne
    lineVTwo = check_direction(pos_2, pos_5, pos_8, player1, player2, board)
    if lineVTwo != BLANK:
        return lineVTwo
    lineVThree = check_direction(pos_3, pos_6, pos_9, player1, player2, board)
    if lineVThree != BLANK:
        return lineVThree
    lineDOne = check_direction(pos_1, pos_5, pos_9, player1, player2, board)
    if lineDOne != BLANK:
        return lineDOne
    lineDTwo = check_direction(pos_3, pos_5, pos_7, player1, player2, board)
    if lineDTwo != BLANK:
        return lineDTwo
    return BLANK
    
    
def print_board(player1, player2, board):
    blank_char = '⬜'
    board_message = ""
    title = 1
    for x in range(len(board)):
        if board[x] == BLANK:
            if title % 3 == 0:
                board_message += blank_char + '\n'
            else:
                board_message += blank_char
        elif board[x] == player1:
            if title % 3 == 0:
                board_message += player1 + '\n'
            else:
                board_message += player1
        elif board[x] == player2:
            if title % 3 == 0:
                board_message += player2 + '\n'
            else:
                board_message += player2
        title += 1
    return board_message


async def get_user_char(ctx, bot, current_player):
    await ctx.send(f'Player {current_player}, choose your character (React with an Emoji).')
    def check_reaction(reaction, user):
        return user != bot.user 
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
    except asyncio.TimeoutError:
        await ctx.send('Timed out.')
        return
    return str(reaction.emoji) 
