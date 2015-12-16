#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <fstream>

int main() {
    	using namespace std;
	std::ifstream infile1("outFinal.txt",std::ifstream::in);
	std::ifstream infile2("outFinal1.txt",std::ifstream::in);
	std::string line1, line2;
	int tp=0,tn = 0, fp = 0,fn = 0, n =0;
	while(std::getline(infile1,line1)){
		if(line1.size()){
	    	std::istringstream iss(line1);
		string id1;
		int bin1;
		if(!(iss >> id1 >> bin1)){
			cout << line1 << "-- " << id1 <<"::" << bin1<< endl;
			break;
		}
		infile2.clear();
		infile2.seekg(0,infile2.beg);
		while(std::getline(infile2,line2)){
			if(line2.size()){
			if(n>0)
				cout << line2;
			std::istringstream iss2(line2);
	                string id2;
        	        int bin2;
                	if(!(iss2 >> id2 >> bin2)){
                        	break;
                	}
			if(!(id1.compare(id2)) && bin1 == bin2){
				tp++;
			}
			else if(!(id1.compare(id2)) && bin1 != bin2){
				fn++;
			}
			else if(id1.compare(id2) && bin1 == bin2){
				fp++;
			}
			}

		}
		tp--;
		}
	}
	cout << "tp:" << tp << endl;
	cout << "tn:" << tn << endl;
	cout << "fp:" << fp << endl;
	cout << "fn:" << fn << endl;
}

