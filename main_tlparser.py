import sys
import re
import streamlit as st


def main():

    file = st.file_uploader(" Upload the TimeLog file here")
    if st.button("Generate"):
        lines = str(file.read(),"utf-8")

        workTime = re.compile(r'((\d{0,1})\d:\d\d)(am|pm)( )*-( )*((\d{0,1})\d:\d\d)(am|pm)')
        timeElapsedInMinutes = 0
        flag = True
        line_number = 0;
        for line in lines:
            line_number += 1
            if (line.find("Time Log") != -1):
              flag = False
              continue
            if flag:
              continue
            line = line.lower()
            line = line.strip()
            if line and workTime.search(line):
              time = workTime.search(line)
              startTime = time.group(1)
              startTimeMeridiem = time.group(3)
              endTime = time.group(6)
              endTimeMeridiem = time.group(8)

              #for start time
              timeString = startTime.split(":")
              if(timeString[0] == "12"):
                timeString[0] = "0"
              startTimeInMinutes = int(timeString[0])*60 + int(timeString[1]) + (0 if startTimeMeridiem=="am" else 720)

              #for end time
              timeString = endTime.split(":")
              if(timeString[0] == "12"):
                timeString[0] = "0"
              endTimeInMinutes = int(timeString[0])*60 + int(timeString[1]) + (0 if endTimeMeridiem=="am" else 720)

              timeElapsedInMinutes += endTimeInMinutes - startTimeInMinutes if endTimeInMinutes > startTimeInMinutes else endTimeInMinutes - startTimeInMinutes + 1440

            else:
              st.write('Could not parse time in line '+str(line_number))
        st.write("Total time author spent : " + str(timeElapsedInMinutes//60) +" hrs " + str(timeElapsedInMinutes%60) + " minutes")

if __name__ == '__main__':
    st.title("Streamlit web app")
    main_bg = "tl_parser.jpg"
    main_bg_ext = "jpg"
    st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    html_temp = """
    <div style="background-color:blue;padding:10px">
    <h2 style="color:white;text-align:center;">Time Log Parser App </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    main()

