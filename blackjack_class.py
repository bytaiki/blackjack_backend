import random

'''
これからも制作を続けて、分けれる部分でのコンポーネント化、フロントエンドの実装、UI UXの向上、デプロイを経てまともに遊べる形にしていきたいです
'''

# Cardクラス
class Card:
    mark = ['hurt','clover','spade','dia']
    def __init__(self):
        self.tramp = []
        for i in self.mark:
            self.tramp.append([i + " " + str(l) for l in range(1,13)])

    def draw(self):
        mark_index = random.randrange(len(self.tramp)) #絵柄決め
        num_index = random.randrange(len(self.tramp[mark_index])) #数字決め
        drawcard = self.tramp[mark_index][num_index]
        self.tramp[mark_index].remove(self.tramp[mark_index][num_index])
        return drawcard

# BlackJackクラス
class BlackJack(Card):
    def __init__(self):
        super().__init__()
        self.players_li = []
        self.players_info = {}
        self.not_bust_players = []

    # 合計値を計算
    def sum(self, draw_li):
        number = 0
        count_ace = 0
        for draw in draw_li:
            split_card = draw.split()
            num = int(split_card[1])
            if num == 1:
                count_ace += 1
                number += 11
            elif num > 10:
                number += 10
            else:
                number += num

        while 1 <= count_ace and number > 21:
            number -= 10
            count_ace -= 1
        return number
    
    # バーストチェック
    def __bust_check(self,number):
        if number > 21:
            return True
        else:
            return False
    
    # 勝敗を返す
    def judge(self,player,dealer):
        if self.__bust_check(player):
            return 'Bust'
        elif self.__bust_check(dealer):
            return 'Win'
        elif player == dealer:
            return 'Draw'
        elif player > dealer:
            return 'Win'
        elif player < dealer:
            return 'Lose'
    
    #ベット額が正しいか
    def player_bet(self,obj,num):
        if obj.chip < num:
            return False
        else:
            return True
    #倍率
    def bairitu(self,obj):
        if len(obj.hand) == 2 and obj.hand_sum == 21:
            return 2.5
        else:
            return 2
    #プレイヤーの入力終了判定
    def player_setting(self,ans):
        if ans == '':
            return True
        else:
            return False

# Playerクラス
class Player:
    def __init__(self):
        self.hand = []
        self.hand_sum = 0
        self.chip = 100
        self.bet = 0

#カードの追加判定
    def player_action(self,num):
        if num == '':
            return False
        elif num == '1':
            return True
        else:
            return 'error'

# Dealerクラス
class Dealer:
    def __init__(self):
            self.hand = []
            self.hand_sum = 0

    def action(self):
        if self.hand_sum >= 17:
            return True
        else:
            return False



# 実際に作った
blackjack = BlackJack()
print('プレイヤーを入力しましょう!')
player_flag = False
while player_flag == False:
    blackjack.players_li.append(input('プレイヤー名を入力してください → '))
    print(f'現在のプレイヤーは{"と".join(blackjack.players_li)}です！')
    u = input('開始する場合、エンターキーを押してください(E)、さらに追加する場合は一文字以上文字を入力ください→ ')
    player_flag = blackjack.player_setting(u)

player_dic = blackjack.players_info #プレイヤーの辞書
players_name = blackjack.players_li #プレイヤーの名前リスト

for player in players_name: #プレイヤーの辞書作成
    player_dic[player] = Player()
    player_dic[player].hand = [blackjack.draw() for _ in range(2)]
    player_dic[player].hand_sum = blackjack.sum(player_dic[player].hand)

while len(players_name) > 0:
    print('======Betのターン======')
    print()


    for player in players_name:
        print(f'{player}さんの現在の所持チップは、{player_dic[player].chip}です！')

    for player in players_name:
        bet_action = False
        while bet_action == False:
            print(f'{player}さんのターン..')
            print(f'持ちチップは、{player_dic[player].chip}です。')
            bet_num = int(input('ベット額を入力してください（数字を入力してください) →  '))
            bet_action = blackjack.player_bet(player_dic[player],bet_num)
            if bet_action:
                player_dic[player].bet = bet_num
                player_dic[player].chip -= bet_num
                print(f'{player}さんは、{player_dic[player].bet}チップをベットしました')
                print(f'{player}さんの残りチップは、{player_dic[player].chip}')
            else:
                print('//無効な入力です、もう一度ベット額を入力ください')

    print('======Playerのターン======')

    print('初期ハンドが配られました')
    for player in players_name:
        print(f'{player}さんの初期ハンドは、{"と".join(player_dic[player].hand)}です 合計値 : {player_dic[player].hand_sum}')
        print()


    dealer = Dealer()
    dealer.hand = [blackjack.draw() for _ in range(2)]
    dealer.hand_sum = blackjack.sum(dealer.hand)
    print(f'ディーラーの初期ハンドは、{dealer.hand[0]} と ？ です')
    print()

    print('= HIT、STANDの選択アクションの開始 =')

    for player in players_name:
        a = input(f'{player}さんのターンです。 :エンターキー(E)で続行')
        draw_action = True
        while player_dic[player].hand_sum < 22 and draw_action:
            print(f'{player}さんの現ハンドは、{"、".join(player_dic[player].hand)}で、')
            print(f'現合計は、 {player_dic[player].hand_sum} です')
            #int(input(f'({player}さん)アクションの選択（数字を入力してください）, 0:STAND 1:HIT →  '))
            action_num = input(f'({player}さん)アクションの選択 → STAND : ENTERキーを押す ,HIT : 1 を入力')
            draw_action = player_dic[player].player_action(action_num)
            if draw_action == 'error':
                print('無効な入力です//')
                print('ENTERキーか、1 で入力してください//')
                draw_action = True
            elif draw_action:
                add_card = blackjack.draw()
                player_dic[player].hand.append(add_card)
                player_dic[player].hand_sum = blackjack.sum(player_dic[player].hand)
                print(f'引いたのは、 {add_card} だよ！')
            if player_dic[player].hand_sum > 21:
                if player_dic[player].chip > 0:
                    print(f'{player}さんはバーストし、{player_dic[player].bet}チップを失いました..')
                    print(f'{player}さんの持ちチップは、{player_dic[player].chip}です')
                else:
                    print(f'{player}さんは、チップが尽きてしまったので退場となります..')
        if player_dic[player].hand_sum <22:
            print(f'{player}さんの最終ハンドは、{player_dic[player].hand_sum} です！')


    print('======Dealerのターン======')

    print(f'ディーラーのハンドは、{"と".join(dealer.hand)}です')

    #バーストしていないプレイヤーリスト作成
    blackjack.not_bust_players = []
    for player in players_name:
        if player_dic[player].hand_sum < 22:
            blackjack.not_bust_players.append(player)
            
    if len(blackjack.not_bust_players) > 0:
        print("さんと".join(blackjack.not_bust_players) + 'さんがディーラーとの勝負です..')

        while True:
            print(f'現在のディーラーの合計値は、{dealer.hand_sum} です')
            a = input()
            if dealer.action():
                break
            aa = blackjack.draw()
            print(f'ディーラーに配られたのは、{aa} です')
            dealer.hand.append(aa)
            dealer.hand_sum = blackjack.sum(dealer.hand)

    print(f'ディーラーの最終合計は、{dealer.hand_sum} です！')

    a = input()#ここまで
    print('======Judge======')
    print('ジャッジします...')
    print()

    for player in blackjack.not_bust_players:
        print(f'{player}の結果は..')
        judge_result = blackjack.judge(player_dic[player].hand_sum,dealer.hand_sum)
        print(f'{player}さんの、{judge_result} です！')
        if judge_result == 'Win':
            print(f'{player}さんの勝ちです！')
            print(f'{int(player_dic[player].bet * blackjack.bairitu(player_dic[player]))}チップを獲得！')
            player_dic[player].chip += int(player_dic[player].bet * blackjack.bairitu(player_dic[player]))
        elif judge_result == 'Draw':
            print(f'{player}さんは、引き分け！')
            print(f'ベットした{player_dic[player].bet}チップが戻されます')
            player_dic[player].chip += player_dic[player].bet
        else:
            print(f'{player}さんは、の負けです..')
            print(f'{player_dic[player].bet}を失いました..')
        if player_dic[player].chip <= 0:
            print(f'{player}さんは、チップが尽きてしまったので退場となります..')
        else:
            print(f'{player}さんの持ちチップは、{player_dic[player].chip}です')
        if player != blackjack.not_bust_players[-1]:
            a = input('エンターキー(E)で続行')

    continue_player = []
    for player in players_name:
        if player_dic[player].chip > 0:
            a = input(f'{player}さんは、ゲームを続行を希望しますか？ する場合 :エンターキーを押す , しない場合 : 1 を入力で終了')
            ans = blackjack.player_setting(a)
            if ans:
                continue_player.append(player)

    players_name = continue_player

    print(players_name)
print('全てのプレイヤーが退出しました。ゲームを終了します。')