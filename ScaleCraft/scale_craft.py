from PIL import Image, ExifTags
import os


class ScaleCraft:

    def __init__(self, path):
        self.image = Image.open(path)
        self.image = self.__fill_bg_white(self.image)
        self.image = self.__rotate(self.image)

        self.filename, ext = os.path.splitext(os.path.basename(path))

    def scale(self, scale):
        """
        画像を指定されたスケールでリサイズします。
        :param scale: スケール値（例：0.5は画像サイズを半分にする）
        :return: スケール後のImageResizerオブジェクト
        """
        # 元の画像の幅と高さを取得
        w, h = self.image.size

        # 新しい幅と高さを計算
        new_width = int(w * scale)
        new_height = int(h * scale)

        # 画像を新しいサイズにリサイズ
        self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # チェーンメソッド化のためにselfを返す
        return self

    def resize(self, max_width, max_height):
        """
        画像を指定された最大幅と高さに収まるようにリサイズします。
        :param max_width: 最大幅
        :param max_height: 最大高さ
        :return: リサイズ後のImageResizerオブジェクト
        """
        # 元の画像の幅と高さを取得
        w, h = self.image.size

        # リサイズする必要があるかどうかを確認
        if w <= max_width and h <= max_height:
            print("No need to resize.")
            return self

        # 画像のアスペクト比を維持しつつリサイズ
        ratio = min(max_width / w, max_height / h)
        new_width = int(w * ratio)
        new_height = int(h * ratio)

        self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return self

    def saveJPEG(self, quality, output_dir, create_dir=True):
        """
        画像をJPEG形式で指定されたディレクトリに保存します。
        :param quality: JPEGの品質（0〜100の整数）
        :param output_dir: 出力ディレクトリのパス
        :param create_dir: 出力ディレクトリが存在しない場合に作成するかどうか
        """
        # 引数の検証
        if not 0 <= quality <= 100:
            raise ValueError("Quality must be between 0 and 100")

        # ディレクトリのフルパスを作成
        full_path = os.path.join(output_dir, self.filename + '.jpg')

        # ディレクトリが存在しない場合は、必要に応じて作成
        if create_dir:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # 画像をJPEG形式で保存
        self.image.save(full_path, 'JPEG', quality=quality)

    def save(self, quality, output_dir):
        self.image.save(output_dir + '/' + self.filename + '.jpg', quality=quality)

    def savePNG(self, quality, output_dir):
        self.image.save(output_dir + '/' + self.filename + '.png', quality=quality)

    def __fill_bg_white(self, image):
        image = image.convert("RGBA")  # it had mode P after DL it from OP
        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, (255, 255, 255))
            background.paste(image, image.split()[-1])  # omit transparency
            return background
        else:
            return image

    def __rotate(self, image):
        """
        スマートフォンからの写真をEXIF情報に基づいて適切に回転させます。
        :param image: PIL Image オブジェクト
        :return: 回転処理が適用された画像
        """
        # EXIF情報を取得し、画像のオリエンテーションを決定
        exifinfo = image.getexif()
        if exifinfo is None:
            return image

        exif_table = {ExifTags.TAGS.get(tag_id, tag_id): value
                      for tag_id, value in exifinfo.items()}

        orientation = exif_table.get('Orientation', 1)

        # オリエンテーションに基づいて画像を回転
        return self.__apply_orientation(image, orientation)

    def __apply_orientation(self, image, orientation):
        """
        指定されたオリエンテーションに基づいて画像を回転します。
        :param image: PIL Image オブジェクト
        :param orientation: EXIFオリエンテーション値
        :return: 回転処理が適用された画像
        """
        operations = {
            2: Image.FLIP_LEFT_RIGHT,
            3: Image.ROTATE_180,
            4: Image.FLIP_TOP_BOTTOM,
            5: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
            6: Image.ROTATE_270,
            7: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_270],
            8: Image.ROTATE_90
        }

        operation = operations.get(orientation, None)
        if operation:
            if isinstance(operation, list):
                for op in operation:
                    image = image.transpose(op)
            else:
                image = image.transpose(operation)

        return image