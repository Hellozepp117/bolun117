#include "some_class.h"

#include <algorithm>    // std::sort
#include <iostream>
MySorter::MySorter(){
	
}
 
 
 bool compareValueIdx (const valueIdx first,const valueIdx second){
     return first.val > second.val;
 }
 bool compareValueIdxSmallestFirst (const valueIdx first,const valueIdx second){
     return first.val < second.val;
 } 
 
int  MySorter::getIndexForTopList(int index, int coordinate){
    
    if (coordinate==0){
        return this->topList[index].s1;
    }else{
        return this->topList[index].s2;
    }
    
}

double  MySorter::getValueForTopList(int index){
    return this->topList[index].val;
}
 
int  MySorter::getOutlierForTopList(int index){
        return this->topList[index].isOutliear;
}
  
double MySorter::computeRi(int sample){
    double inClassDistance=100000;
    double OutClassDistance=100000;
    for (int to=0; to<this->n; to++){
        if(!this->isOutlier[to]){
            
            double distance =  this->computeDistanceBetweenTwoPoint(sample, to);           
            if (this->labels[sample] ==  this->labels[to]){
                if (inClassDistance > distance){
                    inClassDistance = distance; 
                }
            }else{
                if (OutClassDistance > distance){
                    OutClassDistance = distance; 
                }
            }
        }
    }
    return OutClassDistance / (inClassDistance);
} 
 
 
void MySorter::setEpsilon(double value){
   this->epsilon = value;
} 


void MySorter::resetOutliers(){
    for (int sample=0;sample<this->n; sample++){
        this->isOutlier[sample]=0;
    }
}
void MySorter::setOutlier(int idx){
    this->isOutlier[idx]=1;
}
void MySorter::removeOutlier(int idx){
    this->isOutlier[idx]=0;
}




int MySorter::getViolationsForT(){

    this->topList.resize(0);

    int ttp = 0;
    for (int sample = 0; sample < this->n; sample++){
        if (!this->isOutlier[sample]){
            double closestInclassPoint = 10000;
            double closestOutclassPoint = 10000;
            
            double MaxDistance = -10000;
            int idxMaxDistance = -1;            
            
            int idxInClass=-1;
            int idxoutClass=-1;
            for (int to=0;to<this->n; to++){
                if (sample != to && !this->isOutlier[to]){
                    
                    double distance = this->computeDistanceBetweenTwoPoint(sample, to);
//                     if (sample==0 || to == 0)
//                     std::cout << sample<<" "<<to<<" "<<distance<<std::endl;
                    if (distance > MaxDistance){
                        MaxDistance = distance;
                        idxMaxDistance = to;
//                         if (sample==0|| to==0)
//                             std::cout<<"C++3 "<< sample<<" "<<to<<" "<< MaxDistance<<std::endl;
                    }
                    
                    if (this->labels[sample] ==  this->labels[to]){
                        if (distance < closestInclassPoint){
                            closestInclassPoint = distance;
                            idxInClass = to;
//                             if (sample==0|| to==0)
//                             std::cout<<"C++ "<< sample<<" "<<to<<" "<< closestInclassPoint<<std::endl;
                            
                        }
                    }else{
                        if (distance < closestOutclassPoint){
                            closestOutclassPoint = distance;
//                             if (sample==0 || to==0)
//                             std::cout<<"C++2 "<< sample<<" "<<to<<" "<< closestOutclassPoint<<std::endl;
                            idxoutClass = to;
                        }
                    }
                    
                }
            }
                
            if (closestInclassPoint < -EML){
                        this->topList.push_back( valueIdx(sample,idxInClass, closestInclassPoint) );
                         ttp++;
                    }
            if (closestOutclassPoint < -EML){
                        this->topList.push_back( valueIdx(sample,idxoutClass, closestOutclassPoint) );
                         ttp++;
                    }
                    
            if (MaxDistance > 1+EML){
                     this->topList.push_back( valueIdx(sample,idxMaxDistance,  1000+MaxDistance) );
//                      std::cout <<ttp<<" XASSA " << sample<<"  "<< idxMaxDistance <<" "<< MaxDistance<<std::endl;
                         ttp++;
                }
//             
//             
//             
            
                        
            if (closestInclassPoint + this->epsilon <   closestOutclassPoint){
                         this->topList.push_back( valueIdx(sample,idxInClass, closestInclassPoint,0) );
                         ttp++;
            }else{
                            this->topList.push_back( valueIdx(sample,idxoutClass, closestOutclassPoint,1) );
                             ttp++;
                        }
                
            
        }
    }
    
    
    
    return ttp;
    
}

 
int MySorter::computeTopRiPoints(int k){
    int totalPoints = 0; 
    this->topList.resize(0);
    
    for (int sample = 0; sample<this->n;sample++){
        double minInclass = 1000;
        double maxDistance = -1;
        double minOutclass = 1000;
        int idx = -1;
        int icidx=-1;
        int icMidx=-1;
        for (int to=0;to<this->n; to++){
            if (sample != to){
                double distance = this->computeDistanceBetweenTwoPoint(sample, to);
                if (this->labels[sample]==this->labels[to] && minInclass > distance ){
                    minInclass = distance;
                    icidx = to;
                }
                if (  maxDistance < distance ){
                    maxDistance = distance;
                    icMidx = to;
                }
                
                
                if (this->labels[sample]!=this->labels[to] && minOutclass > distance ){
                    minOutclass = distance;
                    idx=to;
                }
//                 if (minOutclass >= 0 ){
//                 }
            }
        }
        this->topList.push_back( valueIdx(sample,idx, minOutclass) );
        totalPoints++;
        if (minInclass<0){
            this->topList.push_back( valueIdx(sample,icidx, minInclass) );
            totalPoints++;
        }
        if (maxDistance>1){
            this->topList.push_back( valueIdx(sample,icMidx, maxDistance) );
            totalPoints++;
        }
    }
   std::sort( this->topList.begin(),this->topList.end(),compareValueIdxSmallestFirst);    
    
    
    return totalPoints;
}


void MySorter::InitializeData(int n, int d){
this->n=n;
this->d=d;	
this->features.resize(n*d,0);
this->B.resize(d*d,0);
this->labels.resize(n,0);
this->isOutlier.resize(n,0);
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

       
