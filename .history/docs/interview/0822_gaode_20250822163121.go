package interview

func FindLargestProduct(nums []float64) float64 {
	if len(nums) == 0 {
		return 0
	}
	dp, rdp := nums[0], nums[0]
	for _, n := range nums[1:] {
		t := dp * n
		rt := rdp * n
		dp = max(t, n)
		rdp = min(rt, n)
	}
	return max(dp, rdp)
}

func main() {
	cases := [][]float64{
		{}
	}
	expect := []float64{

	}
	for i, case := range cases {
		got := FindLaFindLargestProduct(case)
		if got != expect[i] {
			fmt.Println()
		}
	}
}
