#ifndef __SERIAL_LINE_H_
#define __SERIAL_LINE_H_

#define MAX_LEN 100

class SerialLine {
private:
	HardwareSerial serial_;
	unsigned int baud_;
	char term_;
	bool line_complete_;
	int length_;
	char inputBuff_[MAX_LEN];
	char outputBuff_[MAX_LEN];
	char inChar_;
public:
	SerialLine() {
		line_complete_ = false;
		length_ = 0;
	}

	void begin(HardwareSerial &serial, unsigned int baud, char term) {
		// init vars
		serial_ = serial;
		baud_ = baud;
		term_ = term;

		serial_.begin(baud_);
	}

	void read() {
		while(serial_.available()) {
			inChar_ = serial_.read();

			if(inChar_ == term_) {
				inputBuff_[length_] = '\0';
				line_complete_ = true;
				memcpy(outputBuff_, inputBuff_, length_+1);
				length_ = 0;
			} else {
				inputBuff_[length_] = inChar_;
				length_++;
			}
		}
	}

	bool isComplete() {
		return line_complete_;
	}

	char * getLine() {
		if(line_complete_) {
			line_complete_ = false;
			return outputBuff_;
		} else
			return 0;
	}
};

#endif
