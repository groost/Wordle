<?php

class Information {
    public $wordsUsed;
    public $greens;
    public $yellows;
    public $greys;

    function __construct($words, $gns, $ys, $gys) {
        $wordsUsed = $words;
        $greens = $gns;
        $yellows = $ys;    
    }
    
}

class WordleSolver {
    public static function getSixLetterWords() {
        $fileContents = file_get_contents("6 Letter Words.txt");
        $arr = explode("\n", $fileContents);
        return $arr;
    }
    
    public static function getPossibleWords() {
        $fileContents = file_get_contents("PossibleWords.txt");
        $arr = explode("\n", $fileContents);
        return $arr;
    }

    public static function narrowDownCrude($arr, $info) {
        $narrowedArr = $arr;  // Create a copy of the array

        foreach ($info->wordsUsed as $word) {
            $key = array_search($word, $narrowedArr);
            if ($key !== false) {
                unset($narrowedArr[$key]);  // Remove the word from narrowedArr
            }
        }

        $resultArr = [];
        $count = 0;

        foreach($narrowedArr as $position => $word) {
            if(WordleSolver::checkGreens($word, $info->greens) && WordleSolver::checkYellows($word, $info->yellows) && WordleSolver::checkGreys($word, $info->greys)) {
                $resultArr[$count++] = $word;
            }
            // else {
            //     echo json_encode(WordleSolver::checkGreens($word, $info->greens));
            // }
        }

        // $narrowedArr = array_filter($narrowedArr, function($word) use ($info) {
        //     return WordleSolver::checkGreens($word, $info->greens) &&
        //            WordleSolver::checkYellows($word, $info->yellows) &&
        //            WordleSolver::checkGreys($word, $info->greys);
        // });

        return $resultArr;  // Re-index the array
    }

    public static function checkYellows($word, $yellows) {
        // echo json_encode($yellows);
        foreach ($yellows as $position => $letters) {
            if (!WordleSolver::containsAllLetters($word, $letters) || WordleSolver::containsLetterAtPosition($word, $position, $letters)) {
                return false;
            }
        }
        return true;
    }

    public static function checkGreys($word, $greys) {
        return !WordleSolver::containsAnyLetters($word, $greys);
    }

    public static function checkGreens($word, $required_positions) {
        foreach ($required_positions as $position => $letter) {
            if($letter == '') {
                continue;
            }

            if ($word[$position] !== $letter) {
                // echo json_encode("$word doesn't have $letter");
                return false;
            }
        }
        // echo json_encode("has $word");
        return true;
    }

    private static function containsAllLetters($word, $letters) {
        foreach ($letters as $letter) {
            if (strpos($word, $letter) === false) {
                return false;
            }
        }
        return true;
    }

    private static function containsAnyLetters($word, $letters) {
        foreach ($letters as $letter) {
            if (strpos($word, $letter) !== false) {
                return true;
            }
        }
        return false;
    }

    private static function containsLetterAtPosition($word, $position, $letters) {
        foreach ($letters as $letter) {
            if ($word[$position] === $letter) {
                return true;
            }
        }
        return false;
    }

    public static function scoreWord($word, $freqDict) {
        $sm = 0;
        foreach (str_split($word) as $letter) {
            if (substr_count($word, $letter) > 1) {
                $sm -= 10000;
            } elseif (array_key_exists($letter, $freqDict)) {
                $sm += $freqDict[$letter];
            }
        }
        return $sm;
    }
    
    public static function infoTheory($arr) {
        if(count($arr) == 0) {
            return [];
        }
        
        $length = strlen($arr[0]); // Assuming all words in $arr have the same length
    
        $freqTable = array_fill(0, $length, array_fill(0, 26, 0));
    
        foreach ($arr as $word) {
            for ($i = 0; $i < $length; $i++) {
                $charCode = ord($word[$i]) - 97;
                if ($charCode >= 0 && $charCode <= 25) {
                    $freqTable[$i][$charCode]++;
                }
            }
        }
    
        $maxIndeces = array_fill_keys(range('a', 'z'), 0);
    
        for ($i = 0; $i < $length; $i++) {
            for ($j = 0; $j < 26; $j++) {
                $maxIndeces[chr($j + 97)] += $freqTable[$i][$j];
            }
        }
    
        arsort($maxIndeces);
    
        $wordDict = [];
        foreach ($arr as $word) {
            $wordDict[$word] = WordleSolver::scoreWord($word, $maxIndeces);
        }
    
        arsort($wordDict);
    
        $wordArr = array_keys($wordDict);
    
        return $wordArr;
    }

    function getRandomAnswer() {
        $fileContents = file_get_contents("wordle-answers-alphabetical.txt");
        $answers = explode("\n", $fileContents);
        return $answers[array_rand($answers)];
    }
    
    function checkAnswers($words) {
        $fileContents = file_get_contents("wordle-answers-alphabetical.txt");
        $answers = explode("\n", $fileContents);
        $result = [];
        $dbl = false;
    
        foreach ($words as $word) {
            $dbl = false;
            foreach (str_split($word) as $letter) {
                if (substr_count($word, $letter) !== 1) {
                    $dbl = true;
                    break;
                }
            }
    
            if (!$dbl || in_array($word, $answers)) {
                $result[] = $word;
            }
        }
    
        return $result;
    }
    
    function calculateScore($word, $referenceLetters) {
        return count(array_filter(array_map(null, str_split($word), str_split($referenceLetters)), function ($charPair) {
            return $charPair[0] === $charPair[1];
        }));
    }
    
    function rankWordsByScore($wordList, $referenceLetters) {
        usort($wordList, function ($word1, $word2) use ($referenceLetters) {
            return WordleSolver::calculateScore($word2, $referenceLetters) - WordleSolver::calculateScore($word1, $referenceLetters);
        });
        return $wordList;
    }
    
    function getColors($word, $answer) {
        $result = "";
        for ($i = 0; $i < strlen($word); $i++) {
            if ($word[$i] == $answer[$i]) {
                $result .= "2";
            } elseif (strpos($answer, $word[$i]) !== false) {
                $result .= "1";
            } else {
                $result .= "0";
            }
        }
        
        return $result;
    }
    
    function initFromAnswer($words, $answer) {
        $info = new Information([], [], [], []);
        $info->wordsUsed = $words;
        
        for($i = 0; $i < strlen($words[0]); $i++) {
            $info->yellows[$i] = [];
            $info->greens[$i] = "";
        }

        for ($i = 0; $i < count($words); $i++) {
            $word = $words[$i];

            for ($j = 0; $j < strlen($word); $j++) {
                $letter = $word[$j];

                if ($letter == $answer[$j]) {
                    $info->greens[$j] = $letter;
                } elseif (strpos($answer, $letter) !== false) {
                    $info->yellows[$j] = [$letter];
                } else {
                    $info->greys[] = $letter;
                }
            }
        }
    
        return $info;
    }
    
}

$solve = new WordleSolver();
if(isset($_POST["methodName"])) {
    switch($_POST["methodName"]) {
        case "getColors":
            $result = $solve->getColors(json_decode($_POST["words"])[$_POST["count"]], json_encode($_POST["answer"]));
            echo json_encode($result);
            echo json_encode($result);
            break;
        case "getWords":
            $info = $solve->initFromAnswer(json_decode($_POST["words"]), json_decode($_POST["answer"]));

            $arr = $solve->narrowDownCrude(json_decode($_POST["wordArr"]), $info);
            // echo json_encode($arr);

            $arr = $solve->infoTheory($arr);
            echo json_encode($arr[0]);
            break;
    }
}