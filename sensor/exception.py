import sys

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    # error_detail.exc_info() provides the error class and the traceback object which can contains complete details.
    print("exc_tb:", exc_tb)
    file_name = exc_tb.tb_frame.f_code.co_filename
    print("file_name:", file_name)
    print("############################")
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class SensorException(Exception):
    def __init__(self, error_message, error_detail:sys):
        """
        :param error_message: error message in string format
        """
        super().__init__(error_message)

        print("ERROR MESSAGE:", error_message)
        print("ERROR DETAIL:", error_detail)
        print(error_detail.exc_info())

        print("############################")

        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        raise SensorException(e, sys)