#include "some_class.h"


 
MySorter::MySorter(){
	
}
 
 
 bool compareValueIdx (const valueIdx first,const valueIdx second){
     return first.val < second.val;
 }
 
int MySorter::computeTopRiPoints(int k){
    int totalPoints = 0; 
    this->topList.resize(0);
    
    for (int sample = 0; sample<this->n;sample++){
        double minInclass = 1000;
        double minOutclass = 1000;
        int idx = -1;
        for (int to=0;to<this->n; to++){
            if (sample != to){
                double distance = this->computeDistanceBetweenTwoPoint(sample, to);
                if (this->labels[sample]==this->labels[to] && minInclass > distance ){
                    minInclass = distance;
                }
                if (this->labels[sample]!=this->labels[to] && minOutclass > distance ){
                    minOutclass = distance;
                    idx=to;
                }
                if (minOutclass > 0 && minOutclass < minInclass){
                    this->topList.push_back( valueIdx(sample,to,minInclass/minOutclass) );
                    totalPoints++;
                }
                
                
            }
        }
    }
    this->topList.sort(compareValueIdx);    
    
    
    return totalPoints;
}


void MySorter::InitializeData(int n, int d){
this->n=n;
this->d=d;	
this->features.resize(n*d,0);
this->B.resize(d*d,0);
this->labels.resize(n,0);
}

void MySorter::setBij(int i, int j, double value){
  this->B[i*this->d+j] = value;	
}

double MySorter::computeDistanceBetweenTwoPoint(int i,int j){
    double distance = 0;
    for (int k=0;k<this->d;k++){
        for (int l=0;l<this->d;l++){
        distance +=  (this->features[i * d + k] - this->features[j * d + k]) * this->B[k * d + l]
                                * (this->features[i * d + l]
                                - this->features[j * d + l]);              
            
        }
    }
    return distance;
}

void MySorter::computeDistanceVialation(double epsilon){
	
	
	
}


void MySorter::setFeature(int sample, int feature, double value){
  this->features[sample*this->d+feature] = value;	
}
 
void MySorter::setLabel(int sample, int label){
  this->labels[sample] = label;	
}


void MySorter::MethodB(int a){
	
}
int MySorter::GetValA(){
	return this->n+this->d;
}
MySorter::~MySorter(){
	
}

       
