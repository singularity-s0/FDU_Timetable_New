# FDU Timetable
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/Liu-Molin/FDU_Timetable/blob/master/LICENCE)

Timetable exporter for FDU. Automatically login to jwfw.fdu.edu.cn, export as `.ics` file. Hope you enjoy this.

自动登录复旦教务系统读取课表，导出为`.ics`文件

## FDU_Timetable-New Changelog
### Bugfixes to make the awesome project usable again!
- Upgraded protocol to HTTPS to avoid error caused by HTTP 302 redirects
- Fixed Regex Expression to prevent courses from being incorrectly positioned in the timetable
- Now asks user to input semester start date (instead of hardcoding it)
- Added lxml to requirements.txt and removed unused imports
- Various optimizations for production environment

Tested 2021-03-12
Bugfix made together with @w568w

## Usage
- download this
- install requirements: `pip install -r requirements.txt` (you may have to use `pip3` depending on your system)
- then run`python3 fetchdata.py`
- Enter your UIS ID, Password, and semester start date when prompted
- The calander is saved as `fdu_timetable.ics`

**Note:** 

- It's not recommanded to `airdrop` the produced `ics` file to your phone.As the result, these events will be automatically loaded to your calendar, which I'm sure you will not like it. What's more, you can't add tag to these events either.

- The best way to add these events is to send to your email inbox,
  open it on your phone. Recommend to use the ios default mail app.

- 尽量以邮件的方式发送生成的`fdu_timetable.ics`至你的邮箱，iOS使用系统默认邮箱打开

## License
This project is distributed under the `Apache 2.0` License, see [LICENSE](https://github.com/Liu-Molin/FDU_Timetable/blob/master/LICENCE) for more information.

## Acknowledgments
[FDU_Timetable](https://github.com/Molin-L/FDU_Timetable)
