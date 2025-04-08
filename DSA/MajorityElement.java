import java.util.*;

public class MajorityElement {
    public static void main(String[] args) {
        List<Integer> nums = Arrays.asList(1, 2, 2, 2, 1, 3, 3, 3, 3, 3);
//        System.out.println(getMajorityElement(nums));
        System.out.println(getMajorityElementBoyleMoore(nums));
    }

    public static Integer getMajorityElement (List<Integer> nums) {
        HashMap<Integer,Integer> countMap = new HashMap<>();
        for (Integer num : nums) {
            if (!countMap.containsKey(num))
                countMap.put(num, 0);
            countMap.put(num, countMap.get(num) + 1);
        }
        return Collections.max(countMap.entrySet(), Map.Entry.comparingByValue()).getKey();
    }

    public static Integer getMajorityElementBoyleMoore (List<Integer> nums) {
        Integer majorityCount = 0;
        Integer majorityElement = -1;
        for (Integer num : nums) {
            if (majorityCount == 0)
                majorityElement = num;
            majorityCount += num == majorityElement ? 1 : -1;
        }
        return majorityElement;
    }
}
