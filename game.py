import tkinter
import stage
import block

class Game:
    """
    ゲーム全体を管理するクラスです
    このクラスを生成し、start()を呼び出すことで
    ゲームを開始させることができます。
    """

    def __init__(self, title, width, height):
        """
        ゲームの各パラメータの状態を初期化し、
        ゲームを開始させる準備を整えます。

        title: ゲームのタイトル
        width: 画面の幅
        height: 画面の高さ
        """
        self.title = title
        self.width = width
        self.height = height
        self.root = tkinter.Tk()
        self.root.bind('<KeyPress>', self.__input)
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.stage = stage.Stage()
        self.image_block = tkinter.PhotoImage(file='puyo_green.png')
        self.image_fix = tkinter.PhotoImage(file='puyo_jama.png')
        self.image_shadow = tkinter.PhotoImage(file='puyo_purple.png')
        self.image_game_over = tkinter.PhotoImage(file='game_over.png')
        self.speed = 300

    def start(self):
        """
        ゲームを開始させるメソッドです。
        """
        self.__init()

    def __init(self):
        """
        ゲームの初期化を行うメソッドです。
        """
        self.__make_window()
        self.__game_loop()
        self.root.mainloop()

    def __make_window(self):
        """
        ゲームの画面を作成するメソッドです。
        """
        self.root.title(self.title)
        self.canvas.pack()

    def __game_loop(self):
        """
        ゲームのメインロジックを定義するメソッドです。
        """
        self.__update()
        self.__render()
        # y座標が一つ前のところのブロックを空に変える
        if not self.stage.is_end():
            # self.speedミリ秒ごとに自身を呼び出す
            self.root.after(self.speed, self.__game_loop)
        else:
            # Trueを渡さないとデフォルト引数のFalseのままになる
            self.__render(True)

    def __input(self, e):
        """
        ユーザーからの入力処理を定義するメソッドです。
        """
        self.stage.input(e.keysym)

    def __update(self):
        """
        ゲーム全体の更新処理を定義するメソッドです。
        """
        self.stage.update()
        if self.stage.is_fix:
            # 速度を下げる
            self.speed -= 100
            # 以下おまけ
            if self.speed < 0:
                self.speed = 100

    def __render(self, is_end=False):
        """
        ゲームの描画処理を定義するメソッドです。
        """
        self.canvas.delete('block')

        for y in range(stage.Stage.HEIGHT):
            for x in range(stage.Stage.WIDTH):
                # ステージの各マスのデータを取得する
                cell_data = self.stage.data[y][x]

                if is_end:
                    # ゲームオーバー用の画面を描画
                    if cell_data == stage.Stage.FIX:
                        # ゲームオーバーのブロックを描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,      # x座標
                            y * block.Block.SCALE,      # y座標
                            image=self.image_game_over,     # 描画画像
                            anchor='nw',                # アンカー
                            tag='block'
                        )
                else:
                    # プレイ画面を描画

                    if cell_data == stage.Stage.BLOCK:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,      # x座標
                            y * block.Block.SCALE,      # y座標
                            image=self.image_block,     # 描画画像
                            anchor='nw',                # アンカー
                            tag='block'
                        )

                    if cell_data == stage.Stage.FIX:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,      # x座標
                            y * block.Block.SCALE,      # y座標
                            image=self.image_fix,     # 描画画像
                            anchor='nw',                # アンカー
                            tag='block'
                        )

        self.__render_shadow(is_end)

    def __render_shadow(self, is_end=False):
        """
        現在のテトリミノの影を描画するメソッドです。
        """
        type = self.stage.type
        rot = self.stage.rot
        x = self.stage.block.x
        # 影を描画するy座標を取得。
        y = self.stage.shadow_position()

        if not is_end:
            for i in range(block.Block.SIZE):
                for j in range(block.Block.SIZE):
                    if self.stage.block.get_cell_data(type, rot, j, i) == stage.Stage.BLOCK:
                        # ブロックの画像を描画する
                        self.canvas.create_image((j + x) * block.Block.SCALE,
                                                 (i + y) * block.Block.SCALE,
                                                 image=self.image_shadow,
                                                 anchor='nw',
                                                 tag='block'
                                                 )


