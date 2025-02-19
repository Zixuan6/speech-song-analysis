import os
import pandas as pd


def process_csv(input_csv, output_folder):
    """
    解析输入 CSV 文件，并按照 speaker 和 condition 生成新的 CSV 文件。

    参数：
    - input_csv: str, 输入 CSV 文件路径
    - output_folder: str, 输出 CSV 存储路径
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 读取 CSV 文件
    df = pd.read_csv(input_csv, sep=",")  # 如果是逗号分隔, 改为 `,`
    print(df.columns)

    # 确保所需列存在
    required_columns = {"language", "date", "condition", "speaker", "duration", "start", "end", "IOI"}
    if not required_columns.issubset(df.columns):
        print("❌ CSV 文件缺少必要列！")
        return

    # 按 speaker 和 condition 分组
    grouped = df.groupby(["speaker", "condition"])

    for (speaker, condition), group_data in grouped:
        # 获取文件名信息
        language = group_data.iloc[0]["language"]
        date = group_data.iloc[0]["date"]

        # 生成输出文件名
        output_filename = f"{language}_{date}_{condition}_speaker{speaker}_IOI.csv"
        output_filepath = os.path.join(output_folder, output_filename)

        # 保存新的 CSV
        group_data.to_csv(output_filepath, index=False)

        print(f"✅ 生成: {output_filename}")


if __name__ == "__main__":
    # 设定输入 CSV 路径和输出文件夹
    input_csv_file = "/Users/betty/Documents/MATLAB/song_speech_Mandarin/data/IOI/Interval_Mandarinpilot.csv"  # 你的实际 CSV 文件路径
    output_folder = "/Users/betty/Documents/MATLAB/song_speech_Mandarin/data/IOI/"  # 你的输出目录

    # 处理 CSV
    process_csv(input_csv_file, output_folder)

    print("🎉 所有数据处理完成！")

