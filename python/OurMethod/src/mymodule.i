    %module mymodule

    %{
    #include "some_class.h"
    %}

    class MySorter
    {
    public:
        MySorter();
        virtual ~MySorter();
        void InitializeData(int n=0, int d=0);
        void setFeature(int sample=0, int feature=0, double value=0);
		void setBij(int i=0, int j=0, double value=0);
		void setLabel(int sample=0, int label=0);
		double computeDistanceBetweenTwoPoint(int i=0,int j=0);

		int computeTopRiPoints(int k=10);
		int getIndexForTopList(int index=0, int coordinate=0);
        double getValueForTopList(int index=0);

		void computeDistanceVialation(double epsilon=0);
        void MethodB(int a = 5);
        int GetValA();
    };
