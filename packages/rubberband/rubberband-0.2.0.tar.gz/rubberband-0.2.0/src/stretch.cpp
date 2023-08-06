/*
 * stretch.cpp
 *
 *  Created on: 15 Nov 2019
 *      Author: julianporter
 */



#include <algorithm>
#include <chrono>
#include <thread>
#include <map>

#include "stretch.hpp"

static const std::map<int,Stretch::Option> OptionMap = {
	{ 0, RB::OptionWindowLong | RB::OptionPhaseIndependent  | RB::OptionTransientsSmooth},
	{ 1, RB::OptionWindowLong | RB::OptionPhaseIndependent  | RB::OptionDetectorSoft},
	{ 2, RB::OptionPhaseIndependent | RB::OptionTransientsSmooth},
	{ 3, RB::OptionTransientsSmooth},
	{ 4, RB::OptionTransientsMixed},
	{ 5, 0},
	{ 6, RB::OptionWindowShort | RB::OptionPhaseIndependent }
};




void Stretch::debug(const int d) {
	RB::setDefaultDebugLevel(d);
}
Stretch::Option Stretch::makeOptions(const int crispness,const bool formant) {
	if(crispness<0||crispness>6) throw std::runtime_error("Crispness out of range");
	auto option=OptionMap.at(crispness);
	if(formant) option |= RB::OptionFormantPreserved;
	return option;
}

Stretch::Stretch(const long rate,const double ratio,const Stretch::Option opts) : in(), out(),
stretcher(rate,1,opts,ratio,1.0) {}


std::vector<float> Stretch::operator()(const std::vector<float> &input) {
	in.assign(input.begin(),input.end());
	countOut=0;
	out.clear();

	study();
	process();
	return out;
}

void Stretch::study() {
	stretcher.setExpectedInputDuration(in.size());
	auto p=in.data();
	stretcher.study(&p,in.size(),true);
}

void Stretch::process() {
	auto p=in.data();
	stretcher.process(&p,in.size(),true);
	int available=stretcher.available();
	if(available>0) {
		processAvailable(available);
	}
	while ((available=stretcher.available())>= 0) {
		if (available > 0) {
			processAvailable(available);
	    } else {
	        std::this_thread::sleep_for(std::chrono::milliseconds(10));
	    }
	}
}

void Stretch::processAvailable(const int available) {
	std::vector<float> obf(available,0.0);
	auto p=obf.data();
	stretcher.retrieve(&p, available);
	countOut += available;
	std::transform(obf.begin(),obf.end(),obf.begin(),[](const float x) {
		return std::min(1.0f,std::max(-1.0f,x));
	});
	out.insert(out.end(),obf.begin(),obf.end());
}


