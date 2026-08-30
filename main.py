from src.data_prep import NJPADataLoader
from src.DiD_calculation import DiD_Calculation_Print
from src.DiD_t_value_calculation import DiD_t_value_Calculation_Print
from src.FTE1_calculation import FTE_1_Calculation
from src.FTE2_calculation import FTE_2calculation
from src.GAP_calculation import GAP_Calculation_Print
from src.GAP_regression import GAP_Regression_Print
from src.horse_race_regression import Horse_Race_Regression_Print
from src.internal_DiD_calculation import internal_DiD_Calculation_Print
from src.NJ_dummy_regression import NJ_Dummy_Regression_Print
from src.standard_error_DiD_calculation import standard_error_DiD_Calculation_Print


def main():

    # Read the original data
    data_frame = NJPADataLoader().load()


    # MODULE 1 - Variable Construction Check
    
    # First variable I am checking: FTE1 (Full-Time Equivalent) employment 1
    # Full-Time Equivalent is a way to statistically combine full-time and part-time
    # headcounts into one number for each store. This is crucial to check
    # because the entire paper is built on this variable and if it is incorrect
    # it will cause a lot of problems later. (DiD, regressions) FTE1 is the first
    # full-time equivalent employment as it is the data collected during the first survey
    # before the minimum wage increase.
    # The formula for FTE is: FTE1 = EMPFT + NMGRS + 0.5*EMPPT
    # EMPFT = Full-Time Employee
    # EMPPT = Part-Time Employee
    # NMGRS = Number of Managers
    # They assumed each part-time employee as half a worker and assumes each part time
    # employee contributes about half the labor of a full time employee
    FTE_1_Calculation(data_frame)
    # I got values of 20.439 and 23.3312 for New Jersey and Pennsylvania respectively.
    # These values are the same as those in the paper. (Reported in Table 3)

    # FTE2 is the second survey measure, using the same formula with the
    # second-wave values which were recorded after the minimum wage increase.
    # The formula is: FTE2 = EMPFT2 + NMGRS2 + 0.5*EMPPT2
    FTE_2calculation(data_frame)
    # The reported values are approximately 21.03 for New Jersey and 21.17 for
    # Pennsylvania. These values are also the same as those reported in the paper.
    # (Reported in Table 3)

    # The next variable I am going to check is the GAP variable. 
    # The GAP variable measures how much did this store actually have to raise wages. 
    #GAPi = (5.05 - Wi1)/ Wi1
    #Wi1 = the stores wage during wave 1 of surveys 
    #GAP only applies to stores that were paying below $5.05 in Wave 1
    #for stores already paying $5.05, GAP = 0
    #A store that was already paying $5.50 an hour was not affected when 
    # the minimum wage increased, while a store that was paying $4.25 an hour 
    # had a significantly larger jump to make. GAP allows us to measure this jump. 
    # This is an extremely important variable because if GAP reflects a change in 
    # employment that is strong evidence that the minimum wage change itself is the 
    # cause, not something else going on in New Jersey
    GAP_Calculation_Print(data_frame)
    #The calculated GAP values are 0.1152 for New Jersey and 0 for Pennsylvania 
    # which matches the values reported in the paper (Reported in Table 3). The 
    # value for Pennsulvania is 0 because ther was no change in minimum wage in 
    # Pennsylvania, so the GAP variable does not apply to that state.
    
    
    # Module 2 — Difference-in-Differences (DiD) Estimation
    
    # In order to minimize the effect on the data to just the increase in Minimum Wage, 
    # card and Krueger used difference in differences which 
    # in simple terms means they used the differences in a control group 
    # (Pennsylvania) in a formula with the differences in the treated group
    #  (New Jersey wage increase) to calculate the total magnitude of the effect.
    #  This technique eliminates any general trends that are hitting both states. 
    #The formula they used was DiD = New Jersey Difference - Pennsylvania Difference 
    #Each State's respective difference is the difference between the first 
    # FTE and the second FTE.
    DiD_Calculation_Print(data_frame)
    #The DiD estimate returned was 2.7536 which is very close to the value reported in the 
    # paper of 2.76 (Reported in Section III.A ("Differences in Differences")


    # Next card and krueger compared Internal DiD
    # instead of comparing New Jersey to Pennsylvania they compared new jersey to 
    # itself in order to test whether the control group of 
    # Pennsylvania was a good control group. If PA is a good control group,
    # then the stores that were unaffected by the minimum wage increase in NJ should 
    # behave similarly to PA.
    # To do this, NJ stores were split into two groups, low wage stores and high wage 
    # stores. Low wage stores were paying 4.25 (the old minimum wage exactly) and 
    # high wage stores were paying $5.00 or more. the internal DiD formula was 
    # DiDinternal = Low Wage NJ Difference - High Wage NJ Difference
    internal_DiD_Calculation_Print(data_frame)
    #the internal DiD estimate value was not explicitly reported in the paper.
    
    #The next check Card and Kreuger performed was the standard error of the DiD estimate.
    #the standard error measures how much the DiD estimate would very if the experiment
    # was repeated multiple times.
    standard_error_DiD_Calculation_Print(data_frame)
    #the standard error was not explicitly reported in the paper.

    #Card and Krueger reported the t value of the DiD estimate as 2.03 (Section III.A ("Differences in Differences")
    #a t value measures how many standard errors away your estimate is from the 
    #mean. A higher t value means your estimate is more statistically significant
    #the formula for a t value is t = DiD/SE(DiD)
    DiD_t_value_Calculation_Print(data_frame)
    #The calculated t value is 2.1048 which is very close to the the reported DiD estimate
    #and is statistically significant 


    #Module 3 — OLS Regressions
    #So far, all the math has been done using averages to summarize the group of stores 
    # in each state. To better document the extent of the effect of the minimum wage 
    #increase, card and krueger also used regressions to further minimize the effect of
    # other variables and keep it as focused on the minimum wage increase as possible.
    
    #NJ Dummy Regression Model: Table 4 Model A 
    #This is the first regression model in the paper and it also checks the for the 
    #change in average employment while checking for other variables that could affect
    #results.
    #ΔEi​=a+bXi​+c⋅NJi​+εi​ 
    #ΔEi​ = Change in employment for store i (FTE2-FTE1)
    #Nji​ = 1 if store i is in New Jersey, 0 if store i is in Pennsylvania
    #Xi​ =control variabless (chain and if the store is company owned vs a franchise)
    #a = the intercept, model's baseline prediction (NJ=0, all controls = 0)
    #b = the coeffecients showing how much each control variable shifts the predicted change
    #c = what this model is made to estimate, how much being in New Jersey shifts the predicted employment change,
    #  holding chain type and ownership constant
    #εi= the error term
    NJ_Dummy_Regression_Print(data_frame)
    #my results were: My results on the left, Card and Kruegers results on the rightn
    #NJ coefficient	2.2815	≈2.30
    #NJ standard error	1.197	≈1.20
    #NJ t-statistic	1.906	≈1.93
    #N (observations)	351	357
    #There are a few discrepencies to make note of. It was not explicitly stated in the
    #paper how Card and Krueger filtered their data but the closest I was able to get it
    #with python was 351 observations. Secondly, to use dummy variables there must be a
    #baseline which is not explcitly stated in the text, BurgerKing was 
    # used for this model 
    #these results show that New Jersey is borderline significant to the results


    #Gap Regression Specification Model B 
    #the formula: ΔEi​=a′+b′Xi​+c′⋅GAPi​+εi′​
    #it is the exact same structure as the NJ Dummy Regression model except instead of 
    #the NJ variable there is a GAP veriable. Model A measures does simply being in
    #New jersey cause the bigger employment change while Model B measures does the size
    # of a stores GAP variable (how much they had to raise wages) cause a bigger 
    # employment change. instead of measuring GAP as a 0 or 1 as we were before, GAP is 
    #now a continuous measure.
    GAP_Regression_Print(data_frame)
    #my results were; My results	Paper's target
    #GAP coefficient	16.3631	14.92
    #GAP standard error	6.237	6.21
    # GAP t-statistic	2.623	≈2.40 (14.92/6.21)
    #N	351	357
    #small differences due to differences in handling missing wage data but a near match
    #these results show that GAP is significant to the results


    #The Horse Race  Model C 
    #the previous models used regression to check if new Jersey being borderline 
    # significant is due to NJ Stores having higher GAPs or if it is something else that
    #causes New jersey to be significant. Essentially, the NJ Dummy regression checked
    #if being in NJ caused the change in employment, the GAP regression checked if the GAp
    #was significant to the change in Employment, and the horse race is checking if 
    #once GAP is accounted for, NJ still has that borderline significance. 
    #the horse race equation is: ΔEi​=a′′+b′′Xi​+c1​⋅NJi​+c2​⋅GAPi​+εi′′​
    Horse_Race_Regression_Print(data_frame)
    #this is the most important test in the entire paper because it goes against the 
    #most obvious objection: that some other factor caused the increase in employment
    #after running the Horse Race Regression the coefficient dropped from Model 1: 
    #NJ alone to Model 3: The horse Race from 2.2815 to 0.8294, and the t-statistic
    #fell from 1.906 to 0.584 landing inside the paper's own reported
    #range of 0.3 to 0.7 for this specification
    #this means once GAP is accounted for, being located in New Jersey adds no further 
    #explanatory power 
    #this supports the basis of Card and Krueger's entire paper:  the minimum wage 
    # increase itself is the more credible driver of the
    #employment effect.

if __name__ == "__main__":
    main()


