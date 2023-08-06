/*
 * main.hpp
 *
 *  Created on: 15 Nov 2019
 *      Author: julianporter
 */

#ifndef STRETCH_HPP_
#define STRETCH_HPP_

#include <vector>
#include <rubberband/RubberBandStretcher.h>

using namespace RubberBand;
using RB = RubberBandStretcher;




class Stretch {
private:
	std::vector<float> in;
	std::vector<float> out;
	unsigned countOut=0;
	RB stretcher;

	std::vector<double>::iterator it;

	void processAvailable(const int available);

	void study();
	void process();

public:
	using Option = RB::Options;
	static Option makeOptions(const int crispness=5,const bool formant=false);

	static void debug(const int d=0);

	Stretch(const long rate,const double ratio,const Option opts = 0);
	virtual ~Stretch() = default;

	std::vector<float> operator()(const std::vector<float> &input);
};


#endif /* STRETCH_HPP_ */
